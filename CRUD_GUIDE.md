# CRUD Operations Guide

The FUB MCP Server now supports full CRUD (Create, Read, Update, Delete) operations for People/Contacts and Custom Fields.

## People/Contact CRUD Operations

### Create Person

**Tool**: `create_person`

Create a new contact in Follow Up Boss.

**Example**:
```json
{
  "name": "create_person",
  "arguments": {
    "firstName": "John",
    "lastName": "Doe",
    "emails": [
      {
        "value": "john.doe@example.com",
        "type": "home",
        "isPrimary": 1
      }
    ],
    "phones": [
      {
        "value": "555-1234",
        "type": "mobile",
        "isPrimary": 1
      }
    ],
    "source": "Website",
    "assignedUserId": "1",
    "stageId": 2,
    "customFields": {
      "customClosePrice": "500000",
      "customBuyerType": "First Time Buyer"
    },
    "tags": ["hot-lead", "buyer"]
  }
}
```

**Response**:
```json
{
  "id": 12345,
  "name": "John Doe",
  "firstName": "John",
  "lastName": "Doe",
  "emails": [...],
  "phones": [...],
  "created": "2025-01-31T12:00:00Z",
  ...
}
```

### Update Person

**Tool**: `update_person`

Update an existing contact. Only include fields you want to update.

**Example**:
```json
{
  "name": "update_person",
  "arguments": {
    "personId": "12345",
    "name": "John Smith",
    "emails": [
      {
        "value": "john.smith@example.com",
        "type": "home",
        "isPrimary": 1
      }
    ],
    "customFields": {
      "customClosePrice": "600000"
    }
  }
}
```

**Response**: Returns the updated person object.

### Delete Person

**Tool**: `delete_person`

⚠️ **Warning**: This permanently deletes the contact from Follow Up Boss.

**Example**:
```json
{
  "name": "delete_person",
  "arguments": {
    "personId": "12345"
  }
}
```

**Response**: Returns deletion confirmation.

### Read Operations (Already Available)

- `get_person` - Get a specific person by ID
- `get_people` - List people with pagination
- `search_people` - Search for people

## Custom Fields

### Get All Custom Fields

**Tool**: `get_custom_fields`

Retrieve all custom fields available in your Follow Up Boss account.

**Example**:
```json
{
  "name": "get_custom_fields",
  "arguments": {}
}
```

**Response**:
```json
{
  "customFields": [
    {
      "id": "1",
      "name": "customClosePrice",
      "label": "Close Price",
      "type": "number",
      "choices": null
    },
    {
      "id": "2",
      "name": "customBuyerType",
      "label": "Buyer Type",
      "type": "dropdown",
      "choices": ["First Time Buyer", "Repeat Buyer", "Investor"]
    }
  ]
}
```

### Get Specific Custom Field

**Tool**: `get_custom_field`

Get details of a specific custom field by ID.

**Example**:
```json
{
  "name": "get_custom_field",
  "arguments": {
    "customFieldId": "1"
  }
}
```

## Using Custom Fields with People

Custom fields can be included when creating or updating people. Use the **name** (not label) of the custom field as the key.

**Example with Custom Fields**:
```json
{
  "name": "create_person",
  "arguments": {
    "firstName": "Jane",
    "lastName": "Smith",
    "emails": [{"value": "jane@example.com", "type": "home", "isPrimary": 1}],
    "customFields": {
      "customClosePrice": "750000",
      "customBuyerType": "First Time Buyer",
      "customPropertyType": "Single Family Home"
    }
  }
}
```

**Important Notes**:
- Use the custom field **name** (e.g., `customClosePrice`), not the label
- For dropdown fields, use the exact choice value
- For number fields, provide a numeric value (as string)
- For date fields, use ISO format (YYYY-MM-DD)
- For text fields, provide a string value

## Complete CRUD Workflow Example

### 1. Get Available Custom Fields
```json
{
  "name": "get_custom_fields",
  "arguments": {}
}
```

### 2. Create a Person with Custom Fields
```json
{
  "name": "create_person",
  "arguments": {
    "firstName": "Alice",
    "lastName": "Johnson",
    "emails": [{"value": "alice@example.com", "type": "home", "isPrimary": 1}],
    "phones": [{"value": "555-5678", "type": "mobile", "isPrimary": 1}],
    "source": "Referral",
    "customFields": {
      "customClosePrice": "450000",
      "customBuyerType": "Repeat Buyer"
    }
  }
}
```

### 3. Update Custom Fields
```json
{
  "name": "update_person",
  "arguments": {
    "personId": "12345",
    "customFields": {
      "customClosePrice": "475000",
      "customBuyerType": "First Time Buyer"
    }
  }
}
```

### 4. Read Updated Person
```json
{
  "name": "get_person",
  "arguments": {
    "personId": "12345"
  }
}
```

### 5. Delete Person (if needed)
```json
{
  "name": "delete_person",
  "arguments": {
    "personId": "12345"
  }
}
```

## Available Fields for Create/Update

### Standard Fields
- `name` - Full name (string)
- `firstName` - First name (string)
- `lastName` - Last name (string)
- `emails` - Array of email objects
- `phones` - Array of phone objects
- `source` - Lead source (string)
- `assignedUserId` - User ID to assign to (string/number)
- `stageId` - Stage ID (number)
- `tags` - Array of tag strings

### Email Object Structure
```json
{
  "value": "email@example.com",
  "type": "home|work|other",
  "isPrimary": 1 or 0
}
```

### Phone Object Structure
```json
{
  "value": "555-1234",
  "type": "mobile|home|work|other",
  "isPrimary": 1 or 0
}
```

### Custom Fields
- `customFields` - Object with custom field names as keys
- Values depend on custom field type (string, number, date, dropdown choice)

## Error Handling

All CRUD operations include error handling:
- Validation errors return descriptive messages
- API errors are translated to readable format
- Missing required fields return helpful error messages

## Best Practices

1. **Get Custom Fields First**: Before creating people, get the list of custom fields to know the correct field names
2. **Use Field Names**: Always use the custom field `name`, not the `label`
3. **Partial Updates**: When updating, only include fields you want to change
4. **Validate Data**: Check dropdown choice values match available options
5. **Handle Errors**: Always check for errors in the response

## Security Notes

- ⚠️ **Delete is Permanent**: There is no undo for delete operations
- ✅ **Update is Safe**: Updates only modify specified fields
- ✅ **Create is Validated**: FUB validates data before creating
- ✅ **Custom Fields**: Only set custom fields that exist in your account

---

**New Tools Added**: 5 (create_person, update_person, delete_person, get_custom_fields, get_custom_field)  
**Total Tools**: 28 (was 23, now includes full CRUD)

