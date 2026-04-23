# Secure MCP + MySQL Integration Guide

A practical guide to building a **secure AI database gateway using MCP (Model Context Protocol) and MySQL**.
This document explains how to safely allow AI systems to access database information using **stored procedures**, while preventing dangerous database operations.



# 1. Goal

The objective is to allow AI systems to safely query a database without exposing:

* Raw SQL execution
* Sensitive tables
* Write operations
* Full database access

Instead, the AI interacts with the database through **controlled tools mapped to stored procedures**.



# 2. Final Architecture


User
   ↓
AI Assistant
   ↓
Agent / MCP Client
   ↓
MCP Server (FastMCP)
   ↓
Security Layer
   ↓
Stored Procedure Layer
   ↓
MySQL Database


The AI **never directly interacts with SQL**.



# 3. Project Structure

Recommended folder structure:


mcp_demo/
│
├── main.py                # MCP server and tool registration
├── db.py                  # Database connection and procedure execution
├── config.py              # Environment variables and configuration
├── logger.py              # Logging configuration
├── ratelimiter.py         # Query rate limiting
├── .env                   # Secrets (DB credentials)
├── pyproject.toml
└── mcp_server_activity.log




# 4. Required Dependencies

Install required packages:


pip install fastmcp
pip install mysql-connector-python
pip install python-dotenv


Or using `uv`:


uv add fastmcp
uv add mysql-connector-python
uv add python-dotenv




# 5. Database Setup

Create a dedicated database user for MCP.


CREATE USER 'mcp_user'@'localhost'
IDENTIFIED BY 'strong_password';


Grant limited privileges:


GRANT SELECT ON mcp_db.* TO 'mcp_user'@'localhost';
GRANT EXECUTE ON mcp_db.* TO 'mcp_user'@'localhost';


Apply changes:


FLUSH PRIVILEGES;


### Important

Never grant permissions like:


DELETE
DROP
TRUNCATE
ALTER
UPDATE




# 6. Environment Secrets

Never hardcode database credentials.

Create a `.env` file:


DB_HOST=localhost
DB_PORT=3306
DB_NAME=mcp_db
DB_USER=mcp_user
DB_PASSWORD=your_password

MAX_QUERY_ROWS=100
MAX_QUERIES_PER_MINUTE=100


Load environment variables in `config.py`.



# 7. Logging

Every MCP request should be logged.

Example log entry:


2026-03-14 18:01:22 | INFO | Procedure called: getCardNameFilterNLD
2026-03-14 18:01:22 | INFO | Returned rows: 25


Logs help with:

* debugging
* auditing AI behavior
* detecting misuse



# 8. Rate Limiting

Rate limiting protects the database from excessive AI queries.

Example policy:


10 queries per second
100 queries per minute


If the AI exceeds the limit, the request is blocked.

This prevents:

* database overload
* runaway agents
* infinite loops



# 9. Result Size Limiting

Stored procedures may return large datasets.

Limit returned rows:


MAX_QUERY_ROWS = 100


Example:


SELECT * FROM huge_table


If 10,000 rows are returned, MCP will only return the first 100.

Benefits:

* prevents huge AI responses
* reduces token usage
* protects system performance



# 10. Procedure Validation

Before executing a stored procedure:

1. Verify the procedure exists.
2. Check for restricted keywords.

Example restricted keywords:


delete
drop
truncate
update
insert
alter
create


If the procedure name contains any of these, execution is blocked.



# 11. Automatic Procedure Discovery

Instead of manually listing procedures, MCP can automatically discover them.

Query MySQL metadata:


SELECT ROUTINE_NAME
FROM INFORMATION_SCHEMA.ROUTINES
WHERE ROUTINE_SCHEMA='mcp_db'
AND ROUTINE_TYPE='PROCEDURE';


This allows new procedures to automatically become available as tools.



# 12. Procedure Schema Discovery

To identify procedure parameters, query:


INFORMATION_SCHEMA.PARAMETERS


Example result:


Procedure: getCardNameFilterNLD
Parameter: nodename
Type: VARCHAR
Mode: IN


This allows AI systems to understand how to call procedures.



# 13. Dynamic Tool Creation

Each discovered procedure is automatically converted into an MCP tool.

Example tools visible in MCP Inspector:


getCardNameFilterNLD
getSubscriberUsage
getNodeStatistics


This avoids writing a separate tool for each procedure.



# 14. Tool Descriptions

Tool descriptions help the AI understand when to call them.

Descriptions can be retrieved from MySQL:


INFORMATION_SCHEMA.ROUTINES.ROUTINE_COMMENT


Example stored procedure:


CREATE PROCEDURE getSubscriberUsage(...)
COMMENT 'Returns subscriber bandwidth usage'


This description appears in MCP Inspector.



# 15. Secure Execution Flow

Full request lifecycle:


AI Request
   ↓
MCP Tool
   ↓
Rate Limit Check
   ↓
Procedure Name Validation
   ↓
Logging
   ↓
Stored Procedure Execution
   ↓
Row Limit Applied
   ↓
Response Returned




# 16. Critical Security Rule

Never allow the AI to run raw SQL queries.

Dangerous pattern:


User → LLM → generate SQL → execute


Safe pattern:


User → LLM → MCP Tool → Stored Procedure → Database


Stored procedures ensure:

* fixed queries
* controlled output
* safe data access



# 17. Best Practices

Always follow these principles when connecting AI to databases:

1. Use stored procedures only
2. Restrict database permissions
3. Implement rate limiting
4. Limit query results
5. Log all activity
6. Use environment variables for secrets
7. Validate procedures before execution



# 18. Outcome

With this architecture:

* AI can safely access database insights
* Database structure remains protected
* Sensitive operations are blocked
* New procedures automatically become tools

This approach creates a **secure AI-to-database gateway using MCP**.



# 19. Future Improvements

Recommended next steps for production systems:

* Add **JWT authentication for MCP tools**
* Implement **read replicas for AI queries**
* Add **tool-level authorization**
* Implement **query cost limits**
* Add **API gateway security**



# 20. Summary

This setup allows teams to safely integrate AI with databases using:

* MCP
* FastMCP
* Stored Procedures
* Security Layers

The result is a **scalable, secure, and production-ready AI data access architecture**.



