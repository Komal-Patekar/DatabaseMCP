# MCP Database Intelligence Server Architecture

## System Overview

The system exposes database capabilities to AI agents using the Model Context Protocol (MCP).

The MCP server acts as a bridge between:

* AI assistants
* database metadata
* stored procedures
* database exploration tools



# High Level Architecture


AI Agent / MCP Client
        │
        ▼
    MCP Server
   (FastMCP)
        │
        ├── Discovery Tools
        │       (database exploration)
        │
        ├── Dynamic Procedure Tools
        │       (generated from database procedures)
        │
        ▼
   Intelligence Engine
   (procedure metadata + categorization)
        │
        ▼
   Database Access Layer
        │
        ▼
      MySQL Database




# Core Components

## 1. MCP Server (main.py)

The MCP server is created using FastMCP.

Responsibilities:

* initialize the MCP server
* register discovery tools
* register dynamic procedure tools



## 2. Database Access Layer (db.py)

This module manages all database communication.

Responsibilities:

* database connection management
* stored procedure execution
* metadata retrieval
* enforcing result limits

All database interactions pass through this layer.



## 3. Tool Generator (tool_generator.py)

This module dynamically converts database stored procedures into MCP tools.

Steps performed:

1. load procedure metadata from database
2. detect procedure parameters
3. generate MCP tool functions dynamically
4. register tools with the MCP server

This allows the system to automatically support new procedures added to the database.



## 4. Intelligence Engine (intelligence_engine.py)

The intelligence engine analyzes stored procedures to generate metadata.

Capabilities include:

* procedure categorization
* description generation
* parameter analysis

Example categories:

| Procedure Pattern | Category            |
| ------------------| ------------------- |
| GetLinkCount      | Network Analytics   |
| GetWeekData       | Time Analytics      |
| InterfaceLinkType | Interface Analytics |


This metadata helps AI agents understand the purpose of each tool.



## 5. Discovery Tools (discovery_tools.py)

Discovery tools allow AI agents to explore database structure.

Implemented tools:


list_databases
list_tables
describe_table


These tools rely on database metadata from:


INFORMATION_SCHEMA




# Security Architecture

Several safeguards are implemented to ensure safe database interaction.

## Keyword Restrictions

Procedures containing dangerous keywords are blocked.

Examples:


DELETE
DROP
TRUNCATE
UPDATE
INSERT
ALTER




## Query Result Limits

The system limits result size using a configurable value:


MAX_QUERY_ROWS


This prevents large data extraction.



## Rate Limiting

The MCP server enforces request rate limits to prevent excessive usage.



## Restricted Database User

The database user used by the MCP server should only have:


SELECT
EXECUTE


permissions.

This prevents modification of production data.



# Metadata Sources

The system retrieves metadata from MySQL system tables.

Examples:


INFORMATION_SCHEMA.ROUTINES
INFORMATION_SCHEMA.PARAMETERS
INFORMATION_SCHEMA.TABLES
INFORMATION_SCHEMA.COLUMNS


These tables allow the MCP server to automatically understand database structure.



# Example AI Interaction Flow

Example interaction between an AI agent and the database:


list_databases()
        ↓
list_tables()
        ↓
describe_table("interface_stats")
        ↓
GetLinkCount("NodeA")


This allows the AI to explore database structure before executing analytical procedures.



# Extensibility

The system is designed to support additional database objects.

Future extensions may include:


list_views
list_functions
list_triggers
search_tables
explain_query


The modular architecture allows new tools to be added easily.



# Conclusion

This architecture demonstrates how MCP servers can safely expose database capabilities to AI systems.

Key design principles:

• modular architecture
• dynamic tool generation
• metadata driven discovery
• secure database access

This approach enables safe and scalable AI-database integration.


