#!/usr/bin/env python3
"""
Lake Erie Gutter World - Drive Interface
Provides functions to read from the canonical Google Drive folders using connected tools.
"""

from pathlib import Path
import json

# Known Folder IDs (from our earlier work)
CHARACTERS_FOLDER_ID = "15sKeYPBz-qUeL2ngn4xMna7IM9C7iTDd"
IMAGES_FOLDER_ID = "1AYDAJhnqMkwxcxSajdDthirWg3i0oq0i"
AREAS_FOLDER_ID = "1wTAtSzsRbfrdHxUoPfOnxP4UOUetAc-O"  # from earlier audit
ROOT_FOLDER_ID = "1ACEBkur1IokhjVf9izxdVCSwx-96orBV"

def list_characters():
    """List all character .md files in the Characters folder."""
    try:
        from tools.google_drive import list_folder  # Adjust if tool path differs
        items = list_folder(CHARACTERS_FOLDER_ID)
        characters = [item['name'] for item in items if item['name'].endswith('.md')]
        return characters
    except Exception as e:
        return f"Could not list characters: {e}. Using known structure instead."

def read_character(character_id: str):
    """Read a specific character file from Drive."""
    try:
        from tools.google_drive import read_file
        # This is a placeholder — in practice we'd need the file_id
        return f"Reading {character_id}.md from Drive would happen here."
    except Exception as e:
        return f"Drive read not available in this context: {e}"

def get_known_structure():
    return {
        "root_folder_id": ROOT_FOLDER_ID,
        "characters_folder_id": CHARACTERS_FOLDER_ID,
        "images_folder_id": IMAGES_FOLDER_ID,
        "areas_folder_id": AREAS_FOLDER_ID
    }

if __name__ == "__main__":
    print("Lake Erie Gutter World Drive Interface")
    print(json.dumps(get_known_structure(), indent=2))
    print("\nCharacters in Drive (attempt):")
    print(list_characters())