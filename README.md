\# Clover Calc Backend

FastAPI backend service for separated calculator system.

Provide RESTful API for calculator, safe expression evaluation and SQLite database storage.



\## Technology

Python, FastAPI, SQLAlchemy, SQLite, AST safe parsing



\## API List

\- GET /api/health : Service health check

\- POST /api/calculate : Expression calculation and save record

\- GET /api/history : Paginated history query with keyword search

\- DELETE /api/history/{id} : Delete single history record

\- DELETE /api/history : Clear all records



\## Security

Use Python AST module to parse expressions instead of unsafe eval().

Prevent code injection attacks.



\## Code Standard

Follow Python PEP 8 specification.

See codestyle.md for details.



