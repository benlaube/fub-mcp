# Quick Start: Dynamic Discovery in FUB MCP

## What's New?

Your FUB MCP server now has **intelligent discovery**! You can ask natural language questions and the AI will automatically discover how to query your data.

---

## New Tools You Can Use

### 1. `find_data_location` 🔍
**Find anything by keywords**

```javascript
// Find stages
find_data_location({
  keywords: ["lead", "stage"],
  entity_type: "stage"
})

// Find custom fields
find_data_location({
  keywords: ["uuid", "identifier"],
  entity_type: "field"
})

// Find endpoints
find_data_location({
  keywords: ["contact", "people"],
  entity_type: "endpoint"
})

// Search everything
find_data_location({
  keywords: ["deal", "transaction"]
  // Searches all: endpoints, stages, fields, sources
})
```

### 2. `get_schema_hints` 📋
**Learn how to query an endpoint**

```javascript
get_schema_hints({ endpoint: "people" })

// Returns:
// - All available filters
// - All stages with IDs
// - All custom fields
// - Common query examples
```

### 3. Resources 📚
**Read schema information**

- `fub://schema/quick-reference` - ⭐ Start here!
- `fub://schema/endpoints` - All API endpoints
- `fub://schema/custom-fields` - All custom fields

---

## Natural Language Queries That Now Work

### Query 1: "Show me contacts in Lead stage"
**What happens**:
1. AI finds "Lead" stage → ID: 2
2. AI queries: `get_people(stageId=2, limit=10)`
3. You get results!

### Query 2: "Find people with custom field UUID"
**What happens**:
1. AI finds "UUID" custom field
2. AI queries contacts
3. AI filters for those with UUID populated

### Query 3: "What filters can I use on contacts?"
**What happens**:
1. AI calls: `get_schema_hints(endpoint="people")`
2. Shows all 6 filters with examples
3. You learn the options!

### Query 4: "Get deals for a specific person"
**What happens**:
1. AI discovers deals endpoint
2. AI finds personId filter
3. AI queries: `get_deals(personId="12345")`

---

## Try It Now!

### In Cursor IDE

Just ask natural questions:

```
"Show me the last 10 contacts in Lead stage"
"Find contacts assigned to user ID 1"
"What custom fields do I have for contacts?"
"Get tasks that are pending"
"Show me contacts from website source"
```

Cursor's AI will:
1. Read the quick reference
2. Discover what it needs
3. Build the right query
4. Get you the results

### Using the MCP Server Directly

```python
from src.fub_mcp.server import call_tool

# Discover stages
result = await call_tool("find_data_location", {
    "keywords": ["lead", "active"],
    "entity_type": "stage"
})

# Get schema hints
result = await call_tool("get_schema_hints", {
    "endpoint": "people"
})

# Query with filters
result = await call_tool("get_people", {
    "stageId": 2,
    "sort": "-created",
    "limit": 10
})
```

---

## Common Use Cases

### Use Case 1: Find Contacts by Stage

```
You: "Show contacts in Active stage"

AI Process:
1. Discovers Active stage (ID: 115)
2. Queries: get_people(stageId=115)
3. Returns results
```

### Use Case 2: Filter by Multiple Criteria

```
You: "Find contacts in Lead stage assigned to user 1 from website"

AI Process:
1. Discovers Lead stage (ID: 2)
2. Discovers website source (ID: 210)  
3. Queries: get_people(stageId=2, assignedUserId=1, sourceId=210)
4. Returns results
```

### Use Case 3: Discover Custom Fields

```
You: "What custom fields do I have?"

AI Process:
1. Reads: fub://schema/custom-fields
2. Shows all custom fields with types
3. Provides usage examples
```

### Use Case 4: Learn Available Filters

```
You: "What can I filter deals by?"

AI Process:
1. Calls: get_schema_hints(endpoint="deals")
2. Shows: personId, pipelineId, stageId filters
3. Provides examples for each
```

---

## Enhanced Tools

### `get_people` Now Supports

All these filters:
- **stageId** - Filter by stage
- **assignedUserId** - Filter by assigned user
- **sourceId** - Filter by lead source
- **tags** - Filter by tags
- **search** - Search by name/email/phone
- **sort** - Sort order (`-created` = newest first)
- **limit** - Number of results
- **offset** - Pagination

**Example**:
```javascript
get_people({
  stageId: 2,
  assignedUserId: 1,
  sort: "-created",
  limit: 10
})
```

---

## Best Practices

### 1. Start with Discovery
When you don't know the exact field/stage/source:
```javascript
// First, discover
find_data_location({ keywords: ["your", "search", "terms"] })

// Then, query with discovered IDs
get_people({ stageId: <discovered_id> })
```

### 2. Use Schema Hints
When you need to know what's possible:
```javascript
get_schema_hints({ endpoint: "people" })
// Shows all filters, stages, fields, examples
```

### 3. Read Quick Reference
For an overview:
```javascript
read_resource("fub://schema/quick-reference")
// Shows common patterns and examples
```

---

## Tips for Cursor Users

### Tip 1: Be Specific
❌ "Show me data"  
✅ "Show me contacts in Lead stage"

### Tip 2: Use Natural Language
❌ "Execute get_people with stageId=2"  
✅ "Show contacts in Lead stage"

### Tip 3: Ask About Schema
✅ "What filters can I use on contacts?"  
✅ "What custom fields do I have?"  
✅ "What stages are available?"

### Tip 4: Combine Filters
✅ "Show contacts in Active stage assigned to user 1"  
✅ "Find pending tasks for person 12345"  
✅ "Get deals in Under Contract stage"

---

## Troubleshooting

### Q: "I don't see my custom fields"
A: Run `find_data_location({ keywords: ["your field name"], entity_type: "field" })`

### Q: "How do I find a specific stage?"
A: Run `find_data_location({ keywords: ["stage name"], entity_type: "stage" })`

### Q: "What's available to filter by?"
A: Run `get_schema_hints({ endpoint: "people" })` (or "deals", "tasks", etc.)

### Q: "How do I know what sources I have?"
A: Run `find_data_location({ keywords: ["source name"], entity_type: "source" })`

---

## Examples with Results

### Example 1: Find and Query Stage

```javascript
// Step 1: Find
find_data_location({ keywords: ["lead"] })

// Result:
{
  "matches": [{
    "type": "stage",
    "name": "Lead", 
    "id": 2,
    "usage": "Use stageId=2 in get_people"
  }]
}

// Step 2: Query
get_people({ stageId: 2, limit: 10 })

// Result: 10 contacts in Lead stage
```

### Example 2: Discover Filters

```javascript
// Ask
get_schema_hints({ endpoint: "people" })

// Result:
{
  "availableFilters": [
    { "name": "stageId", "type": "number", "example": "stageId=2" },
    { "name": "assignedUserId", "type": "number", "example": "assignedUserId=1" },
    { "name": "sourceId", "type": "number", "example": "sourceId=210" },
    { "name": "tags", "type": "string", "example": "tags='VIP'" },
    { "name": "search", "type": "string", "example": "search='John'" },
    { "name": "sort", "type": "string", "example": "sort='-created'" }
  ],
  "stages": [...],
  "customFields": [...],
  "commonQueries": [...]
}
```

---

## What Makes This Different?

### Before Discovery:
```
❌ Had to know stage IDs
❌ Had to know custom field names
❌ Had to know available filters
❌ Many failed query attempts
```

### After Discovery:
```
✅ AI discovers stage IDs automatically
✅ AI finds custom fields by keywords
✅ AI learns available filters on-demand
✅ Queries work first time
```

---

## Next Steps

1. **Try a query** in Cursor: "Show me contacts in Lead stage"
2. **Explore custom fields**: "What custom fields do I have?"
3. **Learn filters**: "What can I filter contacts by?"
4. **Experiment**: Ask natural questions and see what happens!

---

**That's it!** Your FUB MCP server is now intelligent and can discover what it needs to answer your questions. 🎉

Just ask natural language questions and let the AI figure out how to query your data!

