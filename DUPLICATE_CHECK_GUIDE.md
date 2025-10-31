# Duplicate Check Guide

The FUB MCP Server includes a powerful duplicate checking tool that follows Follow Up Boss's official deduplication rules.

## Overview

The `check_duplicates` tool helps you identify potential duplicate contacts before creating new ones or when managing existing contacts.

## FUB Deduplication Rules

Follow Up Boss uses two main rules to identify duplicates:

1. **Email Address Match**: If two contacts share the same email address, they are considered duplicates.

2. **Phone + Name Match**: If two contacts have the same phone number AND both first and last names match, they are considered duplicates.

## Tool: `check_duplicates`

### Parameters

- **`email`** (optional, string): Email address to check for duplicates
- **`phone`** (optional, string): Phone number to check for duplicates
- **`firstName`** (optional, string): First name (required if checking by phone)
- **`lastName`** (optional, string): Last name (required if checking by phone)
- **`searchLimit`** (optional, number, default: 500): Maximum number of contacts to search. Higher values give more thorough checks but are slower.

**Note**: At least one of `email` or `phone` must be provided. If using `phone`, both `firstName` and `lastName` are required.

### Response Format

```json
{
  "hasDuplicates": true,
  "duplicateCount": 1,
  "searchedContacts": 100,
  "searchCriteria": {
    "email": "john@example.com",
    "phone": null,
    "firstName": null,
    "lastName": null
  },
  "duplicates": [
    {
      "id": 12345,
      "name": "John Doe",
      "firstName": "John",
      "lastName": "Doe",
      "emails": [
        {
          "value": "john@example.com",
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
      "matchReasons": ["email_match"],
      "confidence": "high",
      "created": "2025-10-31T12:00:00Z",
      "source": "Website"
    }
  ]
}
```

### Match Reasons

- **`email_match`**: Email address matches (high confidence)
- **`phone_and_name_match`**: Phone number and both names match (medium confidence)

### Confidence Levels

- **`high`**: Email match found (most reliable)
- **`medium`**: Phone and name match found (reliable if both match)

## Usage Examples

### Example 1: Check by Email Before Creating Contact

```json
{
  "name": "check_duplicates",
  "arguments": {
    "email": "new.lead@example.com",
    "searchLimit": 200
  }
}
```

**Response if duplicate found:**
```json
{
  "hasDuplicates": true,
  "duplicateCount": 1,
  "duplicates": [
    {
      "id": 12345,
      "name": "John Doe",
      "matchReasons": ["email_match"],
      "confidence": "high"
    }
  ]
}
```

### Example 2: Check by Phone and Name

```json
{
  "name": "check_duplicates",
  "arguments": {
    "phone": "555-1234",
    "firstName": "John",
    "lastName": "Doe",
    "searchLimit": 300
  }
}
```

### Example 3: Check Both Email and Phone

```json
{
  "name": "check_duplicates",
  "arguments": {
    "email": "john@example.com",
    "phone": "555-1234",
    "firstName": "John",
    "lastName": "Doe"
  }
}
```

This will check for duplicates using both criteria, potentially finding matches via either method.

## Best Practices

### 1. Check Before Creating

Always check for duplicates before creating a new contact:

```python
# Step 1: Check for duplicates
duplicate_check = await check_duplicates({
    "email": new_contact_email,
    "phone": new_contact_phone,
    "firstName": new_contact_first_name,
    "lastName": new_contact_last_name
})

# Step 2: If duplicates found, update existing instead
if duplicate_check["hasDuplicates"]:
    # Update existing contact or merge data
    update_person(duplicate_check["duplicates"][0]["id"], new_data)
else:
    # Safe to create new contact
    create_person(new_data)
```

### 2. Adjust Search Limit

- **Small databases (< 1000 contacts)**: Use `searchLimit: 500` or higher for thorough checks
- **Large databases (> 10000 contacts)**: Use `searchLimit: 1000` or higher, but be aware it may be slower
- **Quick checks**: Use `searchLimit: 100` for faster results on recent contacts

### 3. Handle Multiple Duplicates

If multiple duplicates are found, review each one:

```python
if duplicate_check["hasDuplicates"]:
    for dup in duplicate_check["duplicates"]:
        # Review each duplicate
        # Decide whether to merge or keep separate
        print(f"Duplicate found: {dup['name']} (ID: {dup['id']})")
        print(f"Confidence: {dup['confidence']}")
        print(f"Match reasons: {dup['matchReasons']}")
```

### 4. Phone Number Normalization

The duplicate checker automatically normalizes phone numbers:
- Removes spaces, dashes, parentheses
- Handles country codes (removes leading "1" for US/Canada)
- Compares on digits only

So these are all treated as the same:
- `555-1234`
- `(555) 123-4567`
- `5551234567`
- `1-555-123-4567`

### 5. Email Normalization

Emails are normalized to lowercase and trimmed, so:
- `John@Example.com` matches `john@example.com`
- ` john@example.com ` matches `john@example.com`

## Integration with Create Person

Example workflow:

```python
# 1. Check for duplicates
duplicate_result = await check_duplicates({
    "email": contact_email,
    "phone": contact_phone,
    "firstName": contact_first_name,
    "lastName": contact_last_name
})

# 2. Handle result
if duplicate_result["hasDuplicates"]:
    # Option A: Update existing contact
    existing_id = duplicate_result["duplicates"][0]["id"]
    await update_person(existing_id, {
        # Add new data or merge
        "customFields": {
            "customSource": "New Lead Source"
        }
    })
    
    # Option B: Skip creation
    print("Duplicate found, skipping creation")
else:
    # Safe to create
    await create_person({
        "firstName": contact_first_name,
        "lastName": contact_last_name,
        "emails": [{"value": contact_email, "isPrimary": 1}],
        "phones": [{"value": contact_phone, "isPrimary": 1}]
    })
```

## Limitations

1. **Search Scope**: The tool searches up to `searchLimit` contacts. For very large databases, you may need to increase this limit or perform multiple searches.

2. **Exact Matches Only**: The tool uses FUB's exact matching rules. Variations in formatting are handled (phone normalization, email normalization), but similar names or partial matches won't trigger duplicate detection.

3. **Name Matching**: For phone-based duplicate detection, both first AND last names must match exactly (after normalization).

## Troubleshooting

### No duplicates found but contact exists

- Check that email/phone formats match (normalization handles most cases)
- Increase `searchLimit` if database is large
- Verify contact actually exists in FUB (use `get_person` or `search_people`)

### Multiple duplicates found

- Review each duplicate's match reasons and confidence
- Check if contacts should be merged or kept separate
- Consider using `update_person` to consolidate data

### Slow performance

- Reduce `searchLimit` for quicker checks
- Use email-based checks when possible (faster than phone+name)
- Search by specific criteria (email OR phone) rather than both if not needed

---

**Tool Name**: `check_duplicates`  
**Added**: v0.4.0  
**Status**: ✅ Fully implemented and tested

