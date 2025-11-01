# Project Structure

Clean, organized structure for the FUB MCP Server.

---

## 📁 Root Directory

```
fub-mcp/
├── README.md                    # Main project documentation
├── QUICKSTART.md               # Quick start guide
├── .env.example                # Example environment variables
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
├── pyproject.toml             # Modern Python config
├── pytest.ini                  # Test configuration
├── cursor_mcp_config.json     # MCP configuration
│
├── src/fub_mcp/               # Source code
│   ├── __init__.py
│   ├── server.py              # Main MCP server
│   ├── tools.py               # Tool definitions
│   ├── fub_client.py          # FUB API client
│   ├── discovery.py           # Dynamic discovery
│   ├── date_filters.py        # Smart date filtering
│   ├── processors.py          # Data processors
│   ├── cache.py               # Caching system
│   ├── config.py              # Configuration
│   └── duplicate_checker.py   # Duplicate detection
│
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   │   ├── test_config.py
│   │   ├── test_crud.py
│   │   ├── test_fub_client.py
│   │   ├── test_processors.py
│   │   └── test_server.py
│   │
│   ├── integration/            # Integration tests
│   │   └── test_integration.py
│   │
│   └── manual/                 # Manual test scripts
│       ├── test_api.py
│       ├── test_caching.py
│       ├── test_discovery_system.py
│       ├── test_smart_dates.py
│       └── ... (14 test scripts)
│
├── scripts/                    # Utility scripts
│   ├── run_server.sh          # Server launcher
│   ├── run_mcp_server.sh      # MCP server launcher
│   ├── list_all_tools.py      # List MCP tools
│   ├── demo_mcp_query.py      # Demo queries
│   ├── check_custom_fields.py # Custom field checker
│   ├── create_uuid_field.py   # UUID field creator
│   ├── verify_uuid_field.py   # UUID verifier
│   └── ... (9 utility scripts)
│
├── examples/                   # Example code
│   ├── basic_usage.py
│   └── crud_example.py
│
└── docs/                       # Documentation
    ├── README.md              # Documentation index
    │
    ├── guides/                # How-to guides
    │   ├── CRUD_GUIDE.md
    │   ├── DUPLICATE_CHECK_GUIDE.md
    │   ├── TESTING.md
    │   ├── CURSOR_SETUP.md
    │   ├── MULTI_CLIENT_SETUP.md
    │   ├── DEPLOYMENT_READY.md
    │   ├── RUN_SERVER.md
    │   └── QUICK_START_DISCOVERY.md
    │
    ├── implementation/         # Technical documentation
    │   ├── DYNAMIC_DISCOVERY_IMPLEMENTATION.md
    │   ├── SMART_DATE_FILTERING.md
    │   ├── IMPROVEMENTS_IMPLEMENTED.md
    │   ├── IMPROVEMENT_ROADMAP.md
    │   ├── CACHING_STRATEGY.md
    │   ├── DYNAMIC_SEARCH_METHOD_GUIDE.md
    │   └── PAGINATION_IMPROVEMENTS.md
    │
    ├── reference/              # API reference
    │   ├── AVAILABLE_TOOLS.md
    │   └── TOOLS_SUMMARY.md
    │
    └── archive/                # Historical documents
        ├── BUILD_PLAN.md
        ├── EXECUTIVE_SUMMARY.md
        ├── PROJECT_STATUS.md
        └── ... (10 archived docs)
```

---

## 📊 File Counts

- **Root files**: 13 (down from 40+!)
- **Source files**: 9
- **Test files**: 20 (organized)
- **Scripts**: 12 (organized)
- **Documentation**: 27 (organized)
- **Examples**: 2

---

## 🎯 Benefits of This Structure

### Clean Root
✅ Only essential files visible  
✅ Easy to find main README  
✅ Clear project overview

### Organized Tests
✅ Unit tests separate from integration  
✅ Manual test scripts in their own folder  
✅ Easy to run specific test types

### Categorized Documentation
✅ **Guides**: How to use features  
✅ **Implementation**: How features work  
✅ **Reference**: API/tool lists  
✅ **Archive**: Historical context

### Grouped Scripts
✅ All utilities in one place  
✅ Server runners easily found  
✅ Development tools organized

---

## 🔍 Finding Things

### "Where is...?"

**Main documentation**:
→ `README.md` in root

**How to get started**:
→ `QUICKSTART.md` in root

**How to do X**:
→ `docs/guides/` (e.g., CRUD_GUIDE.md)

**How does X work**:
→ `docs/implementation/` (e.g., SMART_DATE_FILTERING.md)

**What tools are available**:
→ `docs/reference/AVAILABLE_TOOLS.md`

**Test scripts**:
→ `tests/manual/` for manual tests  
→ `tests/` for unit/integration tests

**Utility scripts**:
→ `scripts/`

**Example code**:
→ `examples/`

---

## 🎓 Navigation Tips

1. **Start** at `README.md`
2. **Quick start** with `QUICKSTART.md`
3. **Learn features** in `docs/guides/`
4. **Deep dive** in `docs/implementation/`
5. **Reference** tools in `docs/reference/`

---

## 📝 Adding New Files

### New Feature?
- Code → `src/fub_mcp/`
- Tests → `tests/unit/` or `tests/integration/`
- Guide → `docs/guides/`
- Implementation details → `docs/implementation/`

### New Script?
- Utility script → `scripts/`
- Example → `examples/`

### New Documentation?
- How-to → `docs/guides/`
- Technical → `docs/implementation/`
- Reference → `docs/reference/`

---

## 🧹 Maintenance

### Keep It Clean
- Archive outdated docs to `docs/archive/`
- Move completed test scripts to appropriate folder
- Update docs index when adding guides
- Keep root directory minimal

### Regular Cleanup
- Review `docs/archive/` for deletion candidates
- Check for duplicate documentation
- Update references when moving files
- Remove obsolete scripts

---

## ✅ Organization Complete!

**Before**: 40+ files in root, mixed tests/docs/scripts  
**After**: 13 clean root files, organized by purpose

**Result**: Professional, maintainable project structure! 🎉

