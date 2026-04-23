# MCP Database Intelligence Server – System Flow

## Example AI Interaction Flow

An AI agent interacts with the database using MCP tools.

```
AI Agent
   │
   ▼
list_databases()
   │
   ▼
list_tables()
   │
   ▼
describe_table("interface_stats")
   │
   ▼
GetLinkCount("NodeA")
   │
   ▼
Database returns results
```

---

## Tool Execution Flow

When a stored procedure tool is called:

```
AI Agent
   │
   ▼
MCP Tool
   │
   ▼
Rate Limiter
   │
   ▼
Procedure Validation
   │
   ▼
Database Execution (call_procedure)
   │
   ▼
Result Limiting
   │
   ▼
Response Returned
```

---

## Discovery Tool Flow

Example for `describe_table`:

```
AI Agent
   │
   ▼
describe_table("table_name")
   │
   ▼
Check if table exists
   │
   ▼
Fetch metadata from INFORMATION_SCHEMA
   │
   ▼
Return column details
```

---

## Security Flow

Security checks applied during execution:

```
Tool Request
   │
   ▼
Rate Limit Check
   │
   ▼
Restricted Keyword Validation
   │
   ▼
Database Execution
   │
   ▼
Result Size Limiting
   │
   ▼
Response Returned
```

These safeguards prevent unsafe database operations.
