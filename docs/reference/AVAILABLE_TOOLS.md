# Available MCP Tools

The FUB MCP Server now provides **23 tools** for interacting with the Follow Up Boss API.

## Main Tool

### ⭐ `execute_custom_query`
The ultimate reporting tool - fetch data from multiple endpoints and process with Python code.

## Individual Endpoint Tools

### 📇 People/Contacts (3 tools)
- **`get_people`** - Get a list of people/contacts with pagination, search, and sorting
- **`get_person`** - Get details of a specific person by ID
- **`search_people`** - Search for people by name, email, or phone

### 📞 Calls (2 tools)
- **`get_calls`** - Get a list of phone calls (optionally filtered by person)
- **`get_call`** - Get details of a specific call by ID

### 📅 Events/Activities (2 tools)
- **`get_events`** - Get a list of events/activities (optionally filtered by person or type)
- **`get_event`** - Get details of a specific event by ID

### 💼 Deals (2 tools)
- **`get_deals`** - Get a list of deals (optionally filtered by person, pipeline, or stage)
- **`get_deal`** - Get details of a specific deal by ID

### ✅ Tasks (2 tools)
- **`get_tasks`** - Get a list of tasks (optionally filtered by person, assigned user, or status)
- **`get_task`** - Get details of a specific task by ID

### 👥 Users/Team Members (3 tools)
- **`get_users`** - Get a list of users/team members
- **`get_user`** - Get details of a specific user by ID
- **`get_me`** - Get current authenticated user information

### 📝 Notes (2 tools)
- **`get_notes`** - Get a list of notes (optionally filtered by person)
- **`get_note`** - Get details of a specific note by ID

### 📆 Appointments (2 tools)
- **`get_appointments`** - Get a list of appointments (optionally filtered by person or date range)
- **`get_appointment`** - Get details of a specific appointment by ID

### 🔄 Pipelines & Stages (4 tools)
- **`get_pipelines`** - Get all pipelines
- **`get_pipeline`** - Get details of a specific pipeline by ID
- **`get_stages`** - Get all stages
- **`get_stage`** - Get details of a specific stage by ID

## Usage Examples

### Using Individual Tools

**Get the most recent contact:**
```json
{
  "name": "get_people",
  "arguments": {
    "limit": 1,
    "sort": "-created"
  }
}
```

**Get a specific person:**
```json
{
  "name": "get_person",
  "arguments": {
    "personId": "12345"
  }
}
```

**Search for people:**
```json
{
  "name": "search_people",
  "arguments": {
    "q": "john@example.com",
    "limit": 10
  }
}
```

**Get calls for a person:**
```json
{
  "name": "get_calls",
  "arguments": {
    "personId": "12345",
    "limit": 50
  }
}
```

**Get user information:**
```json
{
  "name": "get_me",
  "arguments": {}
}
```

### Using the Main Tool (execute_custom_query)

For complex queries combining multiple endpoints and custom processing, use `execute_custom_query`:

```json
{
  "name": "execute_custom_query",
  "arguments": {
    "description": "Team performance report",
    "endpoints": [
      {"endpoint": "/people", "dateField": "created"},
      {"endpoint": "/calls", "dateField": "created"}
    ],
    "dateRange": {
      "start": "2025-06-01",
      "end": "2025-06-30"
    },
    "processing": "result = utils.countBy(data['people'], 'assignedUserId')"
  }
}
```

## Tool Selection Guide

**Use Individual Tools When:**
- You need a simple, quick query
- You want to get a specific item by ID
- You're doing a single endpoint query
- You prefer explicit tool names
- **You're creating, updating, or deleting data** (CRUD operations)

**Use `execute_custom_query` When:**
- You need to combine data from multiple endpoints
- You want custom data processing/aggregation
- You need date filtering across endpoints
- You're building complex reports

## CRUD Tools

**People/Contact Management:**
- `create_person` - Create new contacts with custom fields
- `update_person` - Update existing contacts (including custom fields)
- `delete_person` - Delete contacts (permanent)

**Custom Fields:**
- `get_custom_fields` - Get all available custom fields
- `get_custom_field` - Get specific custom field details

See [CRUD_GUIDE.md](CRUD_GUIDE.md) for detailed examples.

---

**Total Tools**: 28 (1 main + 22 read + 5 CRUD/custom field tools)

