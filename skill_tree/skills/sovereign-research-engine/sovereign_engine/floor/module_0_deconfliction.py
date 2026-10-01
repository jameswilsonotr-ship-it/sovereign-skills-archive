import math
import logging
from typing import List, Dict, Tuple, Optional, Any
from difflib import SequenceMatcher
from sovereign_engine.core.models import GlossaryTerm, TermStatus, VaultState

logger = logging.getLogger("sovereign_engine.floor.module_0")


class ForestFloorDeconflictor:
    """
    Module 0: Deconfliction & Forest Floor Engine.
    Combines lexical fuzzy matching and TF-IDF semantic similarity to detect
    synonymous terms, jargon drift, and dual-layer definitions.
    Constructs cross-link knowledge graphs for Obsidian Canvas export.
    """

    def __init__(self, similarity_threshold: float = 0.75):
        self.similarity_threshold = similarity_threshold

    def deconflict_terms(
        self, new_terms: List[GlossaryTerm], vault_state: VaultState
    ) -> Tuple[List[GlossaryTerm], List[Dict[str, Any]]]:
        """
        Deconflicts incoming GlossaryTerms against the canonical glossary_db in VaultState.
        Returns (merged_and_updated_terms, conflict_reports).
        """
        conflicts = []
        resolved_terms = []

        existing_db = vault_state.glossary_db

        for new_term in new_terms:
            canonical_key = new_term.term.strip().lower()

            # Check exact match
            if canonical_key in existing_db:
                existing_term = existing_db[canonical_key]
                logger.info(f"Exact match found for term '{new_term.term}'. Updating canonical definition.")
                existing_term.status = TermStatus.CANONICAL
                if new_term.canonical_definition:
                    existing_term.canonical_definition = new_term.canonical_definition
                if new_term.eli5_definition:
                    existing_term.eli5_definition = new_term.eli5_definition
                if new_term.technical_definition:
                    existing_term.technical_definition = new_term.technical_definition
                resolved_terms.append(existing_term)
                continue

            # Check semantic/fuzzy duplicate against existing DB
            best_match_key = None
            highest_sim = 0.0

            for existing_key, existing_term in existing_db.items():
                sim = self._calculate_hybrid_similarity(
                    new_term.term, new_term.canonical_definition,
                    existing_term.term, existing_term.canonical_definition
                )
                if sim > highest_sim:
                    highest_sim = sim
                    best_match_key = existing_key

            if highest_sim >= self.similarity_threshold and best_match_key:
                conflict_target = existing_db[best_match_key]
                new_term.status = TermStatus.CONFLICTING
                new_term.conflicts_with = conflict_target.term
                conflict_report = {
                    "new_term": new_term.term,
                    "existing_term": conflict_target.term,
                    "similarity_score": round(highest_sim, 3),
                    "new_definition": new_term.canonical_definition,
                    "existing_definition": conflict_target.canonical_definition,
                    "action_required": "Human Adjudication / Merge"
                }
                conflicts.append(conflict_report)
                logger.warning(f"Semantic conflict detected: '{new_term.term}' vs '{conflict_target.term}' (score: {highest_sim:.2f})")
            else:
                new_term.status = TermStatus.NEW

            # Add to vault glossary DB
            existing_db[canonical_key] = new_term
            resolved_terms.append(new_term)

        return resolved_terms, conflicts

    def _calculate_hybrid_similarity(self, term1: str, def1: str, term2: str, def2: str) -> float:
        """
        Calculates hybrid similarity: 40% term lexical similarity + 60% definition TF-IDF cosine similarity.
        """
        lexical_score = SequenceMatcher(None, term1.lower(), term2.lower()).ratio()
        tfidf_score = self._tfidf_cosine_similarity(def1.lower(), def2.lower())
        return (0.4 * lexical_score) + (0.6 * tfidf_score)

    def _tfidf_cosine_similarity(self, text1: str, text2: str) -> float:
        """Computes TF-IDF cosine similarity between two text snippets."""
        words1 = [w for w in re_words(text1) if len(w) > 2]
        words2 = [w for w in re_words(text2) if len(w) > 2]

        if not words1 or not words2:
            return 0.0

        vocabulary = list(set(words1 + words2))
        if not vocabulary:
            return 0.0

        # Term frequencies
        tf1 = {w: words1.count(w) / len(words1) for w in vocabulary}
        tf2 = {w: words2.count(w) / len(words2) for w in vocabulary}

        # Inverse document frequencies (across 2 docs)
        idf = {}
        for w in vocabulary:
            doc_count = (1 if w in words1 else 0) + (1 if w in words2 else 0)
            idf[w] = math.log(3.0 / (1.0 + doc_count)) + 1.0

        # Vectors
        vec1 = [tf1[w] * idf[w] for w in vocabulary]
        vec2 = [tf2[w] * idf[w] for w in vocabulary]

        dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
        norm1 = math.sqrt(sum(v1 ** 2 for v1 in vec1))
        norm2 = math.sqrt(sum(v2 ** 2 for v2 in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def export_obsidian_canvas(self, vault_state: VaultState) -> Dict[str, Any]:
        """
        Generates an Obsidian Native .canvas JSON layout from the glossary terms and pending leaves.
        """
        nodes = []
        edges = []

        x, y = 0, 0
        node_id_map = {}

        # Add Glossary Nodes
        for term_key, term in vault_state.glossary_db.items():
            nid = f"node_{len(nodes) + 1}"
            node_id_map[term.term.lower()] = nid
            nodes.append({
                "id": nid,
                "type": "text",
                "text": f"### [[{term.term}]]\n**Status**: {term.status}\n\n{term.canonical_definition}",
                "x": x,
                "y": y,
                "width": 300,
                "height": 180,
                "color": "2" if term.status == TermStatus.CONFLICTING else "1"
            })
            x += 350
            if x > 1400:
                x = 0
                y += 220

        # Add Edges for conflicts
        edge_id = 1
        for term_key, term in vault_state.glossary_db.items():
            if term.conflicts_with and term.conflicts_with.lower() in node_id_map:
                from_id = node_id_map[term.term.lower()]
                to_id = node_id_map[term.conflicts_with.lower()]
                edges.append({
                    "id": f"edge_{edge_id}",
                    "fromNode": from_id,
                    "toNode": to_id,
                    "label": "conflicts / duplicate of"
                })
                edge_id += 1

        return {
            "nodes": nodes,
            "edges": edges
        }


def re_words(text: str) -> List[str]:
    import re
    return re.findall(r"\w+", text)
