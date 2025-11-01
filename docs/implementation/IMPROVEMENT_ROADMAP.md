# FUB MCP Server - Improvement Roadmap

Based on the current implementation analysis, here are recommended improvements prioritized by impact and effort.

---

## 🔥 High Impact, Low Effort (Do First)

### 1. **Batch Operations** ⭐
**Problem**: Can only create/update one contact at a time  
**Solution**: Add batch tools for bulk operations

**Impact**: 10x faster for bulk imports  
**Effort**: 2-3 hours

```python
# New tools to add:
- batch_create_people (create multiple contacts)
- batch_update_people (update multiple contacts)
- import_from_csv (bulk import)
```

**Use cases**:
- Import 100 leads from a spreadsheet
- Update 50 contacts with new tags
- Bulk stage changes

---

### 2. **Query Builder Helper** ⭐
**Problem**: Complex queries are hard to construct  
**Solution**: Add a query builder that guides users

**Impact**: Easier query construction, fewer errors  
**Effort**: 3-4 hours

```python
# New tool:
build_query({
  "description": "Find active contacts from website in last 30 days",
  "suggest": true  // AI suggests the query structure
})

# Returns:
{
  "tool": "get_people",
  "arguments": {
    "stageId": 115,  # Active
    "sourceId": 210,  # Website
    "dateFilter": "created > 2024-10-01"
  },
  "explanation": "Query will find contacts in Active stage..."
}
```

---

### 3. **Smart Discovery Caching** ⭐
**Problem**: Stages/custom fields fetched on every discovery  
**Solution**: Cache with 5-minute TTL

**Impact**: 50% faster discovery, fewer API calls  
**Effort**: 1-2 hours

```python
# Cache stages, custom fields, sources for 5 minutes
# Invalidate on create/update operations
# Reduces API calls from 3-4 to 1-2 per query
```

---

### 4. **Advanced Date Filtering** ⭐
**Problem**: No easy way to filter by date ranges  
**Solution**: Add date filter helpers

**Impact**: Common use case becomes trivial  
**Effort**: 2 hours

```python
# Enhanced get_people:
get_people({
  "stageId": 2,
  "createdAfter": "2024-10-01",  # New
  "createdBefore": "2024-10-31",  # New
  "updatedInLast": "7 days"  # New
})
```

---

### 5. **Better Error Messages** ⭐
**Problem**: Generic error messages  
**Solution**: Contextual, actionable errors

**Impact**: Faster debugging, better UX  
**Effort**: 2 hours

```python
# Before:
"400 Bad Request"

# After:
"Invalid stageId: 999. Available stages: Lead (2), Active (115)...
Use find_data_location to discover valid stage IDs."
```

---

## 🚀 High Impact, Medium Effort (Do Next)

### 6. **Relationship Navigator**
**Problem**: Hard to navigate contacts → deals → tasks  
**Solution**: Add relationship traversal tools

**Impact**: Easier multi-entity queries  
**Effort**: 4-5 hours

```python
# New tools:
get_contact_with_relationships({
  "personId": "12345",
  "include": ["deals", "tasks", "events", "notes"]
})

# Returns complete contact with all related data
```

---

### 7. **Fuzzy Search in Discovery**
**Problem**: Typos break discovery ("Realtor" vs "Realty")  
**Solution**: Add fuzzy matching with Levenshtein distance

**Impact**: More forgiving search  
**Effort**: 3-4 hours

```python
# Will match:
"realtor" → "Realtor", "Realty", "Real Estate"
"uuid" → "UUID", "UID", "unique_id"
```

---

### 8. **Query Validation**
**Problem**: Invalid queries sent to API  
**Solution**: Validate before API call

**Impact**: Faster failures, better error messages  
**Effort**: 3-4 hours

```python
# Validates:
- stageId exists
- assignedUserId is valid user
- Custom field types match
- Date formats are correct
```

---

### 9. **Performance Monitoring**
**Problem**: Can't track slow queries  
**Solution**: Add performance metrics

**Impact**: Identify bottlenecks  
**Effort**: 3 hours

```python
# Tracks:
- Query execution time
- API call count
- Cache hit rates
- Slow query warnings
```

---

### 10. **Custom Field Type Validation**
**Problem**: Wrong types in custom fields cause silent failures  
**Solution**: Validate types before saving

**Impact**: Prevent data corruption  
**Effort**: 3 hours

```python
# Validates:
create_person({
  "customFields": {
    "budget_max": 500000,  # Must be number
    "preferred_area": "downtown"  # Must be string
  }
})

# Throws error if types don't match schema
```

---

## 💎 Medium Impact, Low Effort (Quick Wins)

### 11. **Pagination Cursor Support**
**Problem**: Offset pagination is slow for large datasets  
**Solution**: Support cursor-based pagination

**Impact**: Faster for large queries  
**Effort**: 2 hours

---

### 12. **Rate Limit Intelligence**
**Problem**: Hits rate limits unexpectedly  
**Solution**: Smart backoff and warnings

**Impact**: Prevents failures  
**Effort**: 2 hours

---

### 13. **Export Tools**
**Problem**: No easy way to export data  
**Solution**: Add export helpers

**Impact**: Common need  
**Effort**: 2 hours

```python
export_contacts({
  "stageId": 2,
  "format": "csv",  # or "json", "excel"
  "fields": ["name", "email", "phone", "created"]
})
```

---

### 14. **Duplicate Detection on Create**
**Problem**: Might create duplicates  
**Solution**: Auto-check before create

**Impact**: Data quality  
**Effort**: 1 hour (already have duplicate checker!)

---

### 15. **MCP Prompts for Common Workflows**
**Problem**: Users don't know common patterns  
**Solution**: Add workflow prompts

**Impact**: Better discoverability  
**Effort**: 2 hours

```python
# Prompts:
- "Import contacts from CSV"
- "Update contact stage"
- "Bulk tag contacts"
- "Find duplicates"
```

---

## 🔮 Future Enhancements (Nice to Have)

### 16. **Webhooks Support**
Listen for FUB changes in real-time

### 17. **Analytics Dashboard**
Built-in reporting and metrics

### 18. **AI Query Suggestions**
Learn from past queries to suggest new ones

### 19. **Multi-Account Support**
Handle multiple FUB accounts

### 20. **Custom Workflows**
Save and reuse complex query sequences

---

## 📊 Recommended Implementation Order

### Phase 1 (Week 1) - Quick Wins
1. ✅ Smart Discovery Caching (1-2 hours)
2. ✅ Better Error Messages (2 hours)
3. ✅ Duplicate Detection on Create (1 hour)
4. ✅ Advanced Date Filtering (2 hours)

**Total**: 6-7 hours  
**Impact**: Immediate usability improvements

### Phase 2 (Week 2) - Power Features
5. ✅ Batch Operations (2-3 hours)
6. ✅ Query Builder Helper (3-4 hours)
7. ✅ Export Tools (2 hours)
8. ✅ Query Validation (3-4 hours)

**Total**: 10-13 hours  
**Impact**: Handles bulk operations, prevents errors

### Phase 3 (Week 3) - Advanced
9. ✅ Relationship Navigator (4-5 hours)
10. ✅ Fuzzy Search (3-4 hours)
11. ✅ Performance Monitoring (3 hours)
12. ✅ Custom Field Validation (3 hours)

**Total**: 13-15 hours  
**Impact**: Professional-grade features

---

## 🎯 Immediate Next Steps (Do Today)

### Step 1: Smart Discovery Caching (1-2 hours)

```python
# src/fub_mcp/discovery.py
class DiscoveryCache:
    """Cache discovery results with TTL."""
    
    _cache = {}
    _ttl = 300  # 5 minutes
    
    @classmethod
    def get_cached_stages(cls, fub_client):
        # Check cache
        if "stages" in cls._cache:
            cached_at, data = cls._cache["stages"]
            if time.time() - cached_at < cls._ttl:
                return data
        
        # Fetch and cache
        data = await fub_client.get("/stages")
        cls._cache["stages"] = (time.time(), data)
        return data
    
    @classmethod
    def invalidate(cls, key):
        if key in cls._cache:
            del cls._cache[key]
```

**Benefits**:
- 50% fewer API calls
- Faster discovery
- Still fresh (5-min TTL)

---

### Step 2: Better Error Messages (2 hours)

```python
# src/fub_mcp/fub_client.py
async def _request(self, method, endpoint, ...):
    try:
        # ... existing code ...
    except httpx.HTTPStatusError as e:
        # Enhanced error handling
        if e.response.status_code == 400:
            error_data = e.response.json()
            
            # Check for common issues
            if "stageId" in params:
                stages = await self.get("/stages")
                available = [s["name"] for s in stages["stages"]]
                message = (
                    f"Invalid stageId: {params['stageId']}. "
                    f"Available stages: {', '.join(available)}. "
                    f"Use find_data_location to discover stage IDs."
                )
                raise ValidationError(message)
            
            # ... more contextual errors ...
```

**Benefits**:
- Faster debugging
- Self-documenting
- Better user experience

---

### Step 3: Batch Create (2 hours)

```python
# src/fub_mcp/tools.py
Tool(
    name="batch_create_people",
    description="Create multiple contacts at once (up to 100)",
    inputSchema={
        "type": "object",
        "properties": {
            "people": {
                "type": "array",
                "description": "List of contact data objects",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        # ... all person fields ...
                    }
                }
            },
            "checkDuplicates": {
                "type": "boolean",
                "description": "Check for duplicates before creating",
                "default": true
            }
        },
        "required": ["people"]
    }
)
```

**Usage**:
```python
batch_create_people({
  "people": [
    {"name": "John Doe", "email": "john@example.com"},
    {"name": "Jane Smith", "email": "jane@example.com"}
  ],
  "checkDuplicates": true
})
```

**Benefits**:
- 10x faster bulk imports
- Built-in duplicate checking
- Progress reporting

---

## 📈 Success Metrics

After implementing improvements, track:

1. **Discovery Speed**: < 500ms for cached queries
2. **Error Rate**: < 5% of queries fail
3. **API Efficiency**: < 2 API calls per query average
4. **User Success**: 95%+ of natural language queries work
5. **Bulk Performance**: 100 contacts/minute for batch operations

---

## 🔧 Technical Debt to Address

### Minor Issues:
1. Import statements could be organized better
2. Some functions are getting long (> 100 lines)
3. Could use more type hints
4. Test coverage could be expanded

### Not Critical But Nice:
1. Add mypy type checking
2. Add pre-commit hooks
3. CI/CD pipeline
4. Auto-generate API docs

---

## 💡 Innovative Ideas

### 1. **AI Query Optimization**
Learn from successful queries to suggest optimizations

### 2. **Smart Defaults**
Predict what users want based on context

### 3. **Query Templates**
Save complex queries as reusable templates

### 4. **Visual Query Builder**
GUI tool for building complex queries

### 5. **Collaborative Filtering**
"Users who queried X also queried Y"

---

## 🎓 Learning Opportunities

These improvements would teach:
1. **Caching strategies** - TTL, invalidation patterns
2. **Batch processing** - Async operations, progress tracking
3. **Error handling** - User-friendly messages, recovery strategies
4. **Query optimization** - Performance tuning, API efficiency
5. **Type validation** - Schema enforcement, data quality

---

## 📝 Summary

**Recommended Priority Order**:
1. ⭐ Smart Discovery Caching (1-2 hours) - Do now!
2. ⭐ Better Error Messages (2 hours) - Do now!
3. ⭐ Batch Operations (2-3 hours) - Do today!
4. ⭐ Advanced Date Filtering (2 hours) - Do today!
5. 🚀 Query Builder Helper (3-4 hours) - Do this week

**Total time for top 5**: 10-13 hours  
**Impact**: Professional-grade MCP server

The discovery system you have now is **excellent**. These improvements would make it **world-class**.

---

**Question**: Which of these would be most valuable for your use case? I can implement any of them right now! 🚀

