# TruthSleuth Documentation & Override Guidelines

## Overview
TruthSleuth is the automated code arbiter for the RootBase architecture. It enforces code quality, security, and structural standards.

## Project Rules & Overrides
- **Global Rules**: Defined in `truthsleuth/config.py`.
- **Directory-Specific Overrides**: If a specific project or directory requires a different set of rules or exclusion patterns, create a `TRUTHSLEUTH.md` file in the **root of that specific project directory**. 
- **DO NOT** nest override configurations in subdirectories. This ensures centralized discoverability and prevents configuration drift.

## Maintenance & Hygiene
- **Imports**: Avoid circular dependencies. `config.py` is the lowest-level dependency and must never import other `truthsleuth` modules.
- **Reporting**: All issues must be logged via the standardized `reporter.py` to ensure consistency.
- **Loop Prevention**: Any automated analysis, especially if it involves recursive operations (e.g., using Whorl patterns), must implement a depth-limiting mechanism and be checked for potential infinite triggering loops.
