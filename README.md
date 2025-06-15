# 📘 API Documentation: User Activity Logs

This API allows authenticated users to log their actions (like login/logout), retrieve logs, and update log statuses. All endpoints are scoped to the logged-in user.

## 🔐 Authentication Required

All endpoints require the user to be authenticated

## Base URL

```bash
/api/logs/
```

## 📥 Create a New Log

**POST** `/api/logs/`

Creates a new activity log for the authenticated user.

### Request Body

```json
{
  "action": "LOGIN",
  "metadata": {
    "device": "mobile"
  }
}
```

### Response

- **201 Created** on success
- **400 Bad Request** if validation fails

```json
{
  "id": 1,
  "user": 4,
  "action": "LOGIN",
  "metadata": {
    "device": "mobile"
  },
  "status": "PENDING",
  "timestamp": "2025-06-15T10:05:00Z"
}
```

## 📄 Get All Logs (with optional filters)

**GET** `/api/logs/`

Returns a list of the user's logs. Supports optional filters.

### Query Parameters

| Param  | Type   | Description                        |
|--------|--------|------------------------------------|
| action | string | Filter by action type              |
| start  | date   | Filter logs from this timestamp    |
| end    | date   | Filter logs to this timestamp      |

### Example

```sql
GET /api/logs/?action=LOGIN&start=2025-01-01&end=2025-06-30
```

### Response

**200 OK**

```json
[
  {
    "id": 1,
    "user": 4,
    "action": "LOGIN",
    "metadata": {
      "device": "mobile"
    },
    "status": "PENDING",
    "timestamp": "2025-06-15T10:05:00Z"
  }
]
```

✅ **Caching is applied on filtered responses for 60 seconds.**

## 🛠️ Update Log Status

**PATCH** `/api/logs/<id>/`

Updates the status of a specific log.

### Request Body

```json
{
  "status": "DONE"
}
```

### Allowed Statuses

- `"PENDING"`
- `"DONE"`
- `"FAILED"`

### Response

- **200 OK** on success
- **403 Forbidden** if the log doesn't belong to user
- **400 Bad Request** if status is invalid
- **404 Not Found** if log not found

```json
{
  "status": "Updated to DONE"
}
```