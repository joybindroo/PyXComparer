# Agent Instructions & Task Tracking

This file serves as the coordination hub for AI agents working on the PyXComparer project. It ensures continuity, tracks progress, and defines the operational standards for the codebase.

## 🎯 Project Goal
Standardize PyXComparer into a professional, modular Python package with both GUI and CLI interfaces, comprehensive testing, and clear documentation.

## 🛠️ Current Status: Phase 1-5 Implementation
The project has undergone a major transition from a monolithic script to a modular package.

### ✅ Completed Tasks
- [x] **Phase 1: Project Structure**
    - Implemented `src/` layout.
    - Added `pyproject.toml` and `requirements.txt`.
    - Created `config.py` and `exceptions.py`.
- [x] **Phase 2: Code Standardization**
    - Modularized logic into `converter.py`, `comparator.py`, and `reporter.py`.
    - Added Python 3.10+ type hints and Google-style docstrings.
- [x] **Phase 3: Feature Expansion**
    - Developed full CLI using `click`.
    - Added JSON report generation.
    - Implemented batch processing and summary commands.
- [x] **Phase 4: Quality Assurance**
    - Created `tests/` suite with `pytest`.
    - Implemented unit tests for converter and comparator.
- [x] **Phase 5: Documentation**
    - Rewrote `README.md` with comprehensive usage guides.
    - Created `CHANGELOG.md`.

## 📋 Pending Tasks / Roadmap
- [ ] **GUI Enhancements**: Implement side-by-side diff view in the GUI.
- [ ] **Export Options**: Add PDF report export.
- [ ] **Performance**: Optimize conversion for extremely large XLSForms.
- [ ] **Integration**: Explore ODK Central API integration for automatic form fetching.

## 🤖 Agent Guidelines
When working on this repository, agents must:
1. **Maintain Modularity**: Do not revert to monolithic files. Keep logic in `src/pyxcomparer/`.
2. **Type Safety**: Always use type hints for function signatures.
3. **Test First**: Any new feature must be accompanied by a corresponding test in `tests/`.
4. **Config Driven**: Use `src/pyxcomparer/config.py` for any constants or default settings.
5. **Documentation**: Update `README.md` and `CHANGELOG.md` when adding new public-facing features.

## 📝 Task Log
- **2026-04-18**: Completed Phases 1-5 (Standardization, CLI, Tests, Docs).
