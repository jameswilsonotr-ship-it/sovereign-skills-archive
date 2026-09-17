"""Deterministic, dependency-free OpenSpec scenario corpus and tooling."""

from .scenario_schema import (
    GENERATOR_VERSION,
    SCENARIO_COUNT,
    SCHEMA,
    SCHEMA_VERSION,
    SEED,
    ScenarioError,
    validate_scenario,
)

__all__ = [
    "GENERATOR_VERSION",
    "SCENARIO_COUNT",
    "SCHEMA",
    "SCHEMA_VERSION",
    "SEED",
    "ScenarioError",
    "validate_scenario",
]
