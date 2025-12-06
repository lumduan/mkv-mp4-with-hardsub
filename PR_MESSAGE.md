# ✨ Refactor: YAML Configuration with Interactive CLI Manager

## 🎯 Overview

This PR introduces a comprehensive YAML-based configuration system with an interactive CLI manager, replacing hard-coded settings with a flexible, user-friendly configuration approach.

## 🚀 Key Features

### 1. YAML Configuration System
- **Type-safe configuration** using Pydantic models for validation
- **Environment variable overrides** with `CONVERTER_` prefix
- **Nested configuration structure** for video, audio, and subtitle settings
- **Default values** with automatic fallbacks
- **Comprehensive validation** for all configuration parameters

### 2. Interactive Config Manager (`scripts/config_manager.py`)
- **🆕 Quick Setup Wizard**: Guided step-by-step configuration for first-time users
  - Quality presets: High Quality, Balanced, Smaller Files
  - Subtitle configuration with language selection
  - Performance settings (parallel processing)
  - Directory path setup
- **Advanced Menu System**:
  - View current configuration
  - Update settings by category (directories, video, audio, subtitles, processing)
  - Built-in help system (Press H) with detailed explanations
  - Real-time validation before saving
  - Reset to defaults option
- **User-friendly interface** with emoji icons and clear prompts

### 3. Enhanced Documentation
- Updated README with Quick Setup Wizard examples
- Comprehensive configuration guide
- Help system with common presets and recommendations
- Project plan updated with Phase 1 completion status

## 📋 Changes Made

### New Files
- `src/config.py` - Configuration models and validation
- `scripts/config_manager.py` - Interactive CLI tool
- `config.yaml` - YAML configuration file with detailed comments

### Modified Files
- `README.md` - Added configuration manager documentation
- `docs/plans/project-plan.md` - Updated Phase 1 status
- `pyproject.toml` - Added pydantic, pydantic-settings dependencies
- `.python-version` - Changed from 3.14 to 3.13 for stability

### Technical Improvements
- ✅ Fixed Python 3.14 alpha compatibility issues
- ✅ Pydantic v2 validation for all settings
- ✅ YAML parsing with PyYAML
- ✅ Interactive input with smart defaults
- ✅ Cross-platform path handling with pathlib

## 🎬 Usage Examples

### Quick Setup (First-Time Users)
```bash
.venv/bin/python scripts/config_manager.py
# Follow the Quick Setup Wizard prompts
```

### Advanced Configuration
```bash
.venv/bin/python scripts/config_manager.py
# Choose option 4 to update video settings
# Choose option H for help and tips
```

### Direct YAML Editing
```bash
nano config.yaml  # Edit configuration manually
```

## 🧪 Testing

- ✅ Tested on Python 3.13.8
- ✅ Configuration validation working
- ✅ Quick Setup Wizard functional
- ✅ All menu options tested
- ✅ Help system verified
- ✅ YAML loading/saving confirmed

## 📚 Documentation

All documentation has been updated to reflect the new configuration system:
- README includes Quick Setup Wizard examples
- Project plan shows Phase 1 completion
- Config manager includes built-in help system
- YAML file has comprehensive inline comments

## 🔄 Migration Notes

For existing users (when applicable):
- Configuration is now in `config.yaml` instead of hard-coded
- Run the Quick Setup Wizard to generate your first configuration
- All previous settings can be configured through the interactive manager
- Environment variables can override any YAML setting

## ✅ Checklist

- [x] Code follows project style guidelines
- [x] Documentation updated (README, project plan)
- [x] Interactive help system implemented
- [x] Real-time validation working
- [x] Python 3.13 compatibility verified
- [x] Dependencies updated in pyproject.toml
- [x] Quick Setup Wizard tested
- [x] All menu options functional

## 🎉 Benefits

1. **User-Friendly**: No code editing required for configuration
2. **Validated**: All inputs validated before saving
3. **Documented**: Built-in help explains all settings
4. **Flexible**: YAML, environment variables, or interactive CLI
5. **Type-Safe**: Pydantic ensures correct data types
6. **Guided**: Quick Setup Wizard for beginners

## 📸 Screenshots

The config manager provides:
- Welcome screen with tips
- Quality preset selection (3 options)
- Guided subtitle configuration
- Performance settings
- Full configuration preview before saving
- Interactive help system

## 🔗 Related Issues

- Implements configuration system from project plan Phase 1
- Addresses need for user-friendly setup process
- Provides foundation for future features (parallel processing, etc.)

---

**Ready for Review** ✨

This PR completes Phase 1 of the project plan and sets up the foundation for batch video conversion with a robust, user-friendly configuration system.
