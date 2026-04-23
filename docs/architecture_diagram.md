# MCP Database Intelligence Server – Architecture Diagram

## System Architecture

The MCP server acts as a bridge between AI agents and the database.

```
AI Agent / MCP Client
        │
        ▼
    MCP Server
   (FastMCP)
        │
        ├───────────────┬────────────────
        │               │
        ▼               ▼
Discovery Tools     Procedure Tools
(database exploration) (dynamic generation)
        │               │
        └───────────────┘
                │
                ▼
        Intelligence Engine
      (procedure metadata analysis)
                │
                ▼
        Database Access Layer
              (db.py)
                │
                ▼
           MySQL Database
```

## Component Responsibilities

### MCP Server

* registers all tools
* exposes tools to AI agents
* handles requests

### Discovery Tools

Allow AI agents to explore database structure.

Examples:

* list_databases
* list_tables
* describe_table

### Dynamic Procedure Tools

Automatically convert database stored procedures into MCP tools.

### Intelligence Engine

Analyzes procedures to generate:

* categories
* descriptions
* metadata

### Database Layer

Handles:

* database connections
* stored procedure execution
* metadata queries

---

