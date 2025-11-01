# Project Reorganization Plan

## Current Issues
- 20+ markdown files in root directory
- 15+ test files scattered in root
- Multiple utility scripts mixed with main files
- Log files and data files in root
- Redundant/outdated documentation

---

## Proposed Structure

```
fub-mcp/
├── README.md                    # Main documentation (KEEP)
├── QUICKSTART.md               # Quick start guide (KEEP)
├── .env.example                # Example env (rename from env.example)
├── requirements.txt
├── setup.py
├── pyproject.toml
├── pytest.ini
├── cursor_mcp_config.json
├── fub_mcp_server.log         # Auto-generated (add to .gitignore)
│
├── src/fub_mcp/               # Source code (existing)
│
├── tests/                      # ALL tests here
│   ├── unit/                   # Unit tests (existing test_*.py)
│   ├── integration/            # Integration tests
│   └── manual/                 # Manual test scripts
│
├── scripts/                    # Utility scripts
│   ├── check_custom_fields.py
│   ├── create_uuid_field.py
│   ├── verify_uuid_field.py
│   ├── download_last_5_people.py
│   ├── estimate_data_size.py
│   ├── measure_cache_size.py
│   ├── list_all_tools.py
│   ├── demo_mcp_query.py
│   ├── get_recent_contact.py
│   └── push_to_remote.sh
│
├── examples/                   # Example usage (existing)
│
└── docs/                       # ALL documentation
    ├── guides/
    │   ├── QUICKSTART.md       # Symlink to root
    │   ├── SETUP.md
    │   ├── TESTING.md
    │   ├── CRUD_GUIDE.md
    │   ├── DUPLICATE_CHECK_GUIDE.md
    │   └── DEPLOYMENT.md
    │
    ├── implementation/
    │   ├── CACHING_STRATEGY.md
    │   ├── DYNAMIC_DISCOVERY_IMPLEMENTATION.md
    │   ├── SMART_DATE_FILTERING.md
    │   └── PAGINATION_IMPROVEMENTS.md
    │
    ├── reference/
    │   ├── AVAILABLE_TOOLS.md
    │   ├── TOOLS_SUMMARY.md
    │   └── API_REFERENCE.md
    │
    └── archive/                # Outdated/superseded docs
        ├── BUILD_PLAN.md
        ├── EXECUTIVE_SUMMARY.md
        ├── PROJECT_STATUS.md
        ├── FIX_CURSOR_ERROR.md
        ├── GITHUB_DEPLOY_SUCCESS.md
        └── ...summaries...
```

---

## Documentation Status Analysis

### ✅ KEEP & ORGANIZE

**Root (Keep in Root)**:
- `README.md` - Main docs
- `QUICKSTART.md` - Quick start

**guides/** (How-to guides):
- `CRUD_GUIDE.md` ✅ Current
- `DUPLICATE_CHECK_GUIDE.md` ✅ Current
- `TESTING.md` ✅ Current
- `CURSOR_SETUP.md` ✅ Current
- `MULTI_CLIENT_SETUP.md` ✅ Current
- `DEPLOYMENT_READY.md` ✅ Current
- `RUN_SERVER.md` ✅ Current

**implementation/** (Technical docs):
- `DYNAMIC_DISCOVERY_IMPLEMENTATION.md` ✅ Current (Nov 1)
- `IMPROVEMENTS_IMPLEMENTED.md` ✅ Current (Nov 1)
- `SMART_DATE_FILTERING.md` ✅ Current (Nov 1)
- `IMPROVEMENT_ROADMAP.md` ✅ Current (Future plans)
- `CACHING_STRATEGY.md` ✅ Current
- `DYNAMIC_SEARCH_METHOD_GUIDE.md` ✅ Current
- `PAGINATION_IMPROVEMENTS.md` ✅ Current

**reference/** (Reference docs):
- `AVAILABLE_TOOLS.md` ✅ Current
- `TOOLS_SUMMARY.md` ✅ Current

### ⚠️ ARCHIVE (Outdated/Superseded)

**Summaries (Redundant)**:
- `SUMMARY.md` - Outdated overview
- `EXECUTIVE_SUMMARY.md` - Initial summary
- `CACHING_SUMMARY.md` - Superseded by CACHING_STRATEGY
- `CRUD_SUMMARY.md` - Superseded by CRUD_GUIDE
- `PAGINATION_AND_DUPLICATES_SUMMARY.md` - Superseded

**Old Implementation Docs**:
- `BUILD_PLAN.md` - Initial planning (complete)
- `PROJECT_STATUS.md` - Point-in-time status
- `FIX_CURSOR_ERROR.md` - Resolved issue
- `GITHUB_DEPLOY_SUCCESS.md` - One-time event
- `DUPLICATE_CHECKER_APPROACH.md` - Superseded by guide

**Outdated Guides**:
- `QUICKSTART.md` vs `QUICK_START_DISCOVERY.md` - Consolidate?

---

## Files to Move

### Tests (15 files) → /tests/manual/
- `test_api.py`
- `test_caching.py`
- `test_create_contact.py`
- `test_create_debug.py`
- `test_discovery_system.py`
- `test_duplicate_check.py`
- `test_improvements.py`
- `test_mcp_stage_query.py`
- `test_memory_usage.py`
- `test_pagination_1000.py`
- `test_pagination_small.py`
- `test_smart_dates.py`
- `test_stage_filtering.py`
- `test_stage_query.py`

### Scripts (10 files) → /scripts/
- `check_custom_fields.py`
- `create_uuid_field.py`
- `verify_uuid_field.py`
- `download_last_5_people.py`
- `estimate_data_size.py`
- `measure_cache_size.py`
- `list_all_tools.py`
- `demo_mcp_query.py`
- `get_recent_contact.py`
- `push_to_remote.sh`

### Docs (20+ files) → /docs/
See structure above

### Data Files → Keep or .gitignore
- `fub_mcp_server.log` - Add to .gitignore
- `last_5_people_20251031_160847.json` - Move to scripts/data/
- `run_mcp_server.sh` - Move to scripts/ or root?
- `run_server.sh` - Move to scripts/ or root?

---

## .gitignore Updates

Add:
```
# Logs
*.log
fub_mcp_server.log

# Data dumps
*.json
!cursor_mcp_config.json

# Test outputs
test_output/
```

---

## README.md Updates

Should reference:
- `QUICKSTART.md` for getting started
- `docs/guides/` for how-to guides
- `docs/implementation/` for technical details
- `docs/reference/` for API reference
- `examples/` for code examples

---

## Migration Steps

1. ✅ Create folders (docs, scripts, tests subdirs)
2. Move test files
3. Move script files
4. Organize docs into subfolders
5. Archive outdated docs
6. Update README with new structure
7. Update .gitignore
8. Update import paths if needed
9. Test everything still works
10. Commit reorganization

---

## Benefits

✅ **Cleaner root**: Only essential files visible  
✅ **Better navigation**: Logical folder structure  
✅ **Clear documentation**: Guides vs Implementation vs Reference  
✅ **No confusion**: Archived old docs  
✅ **Professional**: Standard project layout  

---

## Questions

1. **QUICKSTART.md duplication?**
   - We have `QUICKSTART.md` and `QUICK_START_DISCOVERY.md`
   - Merge or keep separate?

2. **Run scripts in root or scripts/?**
   - `run_server.sh` and `run_mcp_server.sh`
   - Common to keep in root for easy access?

3. **Keep examples/ in root?**
   - Yes, standard for Python projects

4. **README stays in root?**
   - YES! Never move README.md

---

## Recommended Actions

**Immediate** (Do now):
1. Move all test_*.py to tests/manual/
2. Move utility scripts to scripts/
3. Create docs/ structure
4. Archive outdated docs

**Soon** (After testing):
1. Consolidate QUICKSTART files
2. Update README with new structure
3. Add comprehensive .gitignore

**Optional** (Nice to have):
1. Create docs index (docs/README.md)
2. Add changelog (CHANGELOG.md)
3. Versioning strategy

