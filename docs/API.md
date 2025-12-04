# API Documentation

## REST API Endpoints

Base URL: `http://localhost:8000`

### Health Check

```bash
GET /health
```

Returns:
```json
{
  "status": "healthy",
  "notion_connected": true,
  "modules_count": 150
}
```

### List All Modules

```bash
GET /api/modules
```

Returns all modules grouped by type.

### Get Specific Module

```bash
GET /api/modules/{module}
```

Parameters:
- `module`: Module letter (A-M) or full name

Example:
```bash
curl http://localhost:8000/api/modules/B
```

### Search

```bash
GET /api/search?query={query}&max_results={limit}
```

Parameters:
- `query`: Search term (required)
- `max_results`: Max results (1-100, default: 20)

Example:
```bash
curl "http://localhost:8000/api/search?query=docker&max_results=10"
```

### Get Command

```bash
GET /api/command/{page_id}
```

Returns full page content.

### Filter by Tag

```bash
GET /api/tags/{tag}
```

Valid tags: Core, Erweitert, Optimierung, Visualisierung, Analyse

### Filter by Type

```bash
GET /api/types/{type}
```

Valid types: Dokumentation, Beispiel, Test, Referenz

### Statistics

```bash
GET /api/statistics
```

Returns statistics about the codex.

### Clear Cache

```bash
POST /api/cache/clear
```

Clears the LRU cache.

## MCP Tools

Available via MCP protocol:

1. **list_modules** - List all modules
2. **get_module** - Get module details
3. **get_command** - Load page content
4. **search** - Search codex
5. **get_by_tag** - Filter by tag
6. **get_by_type** - Filter by type
7. **get_statistics** - Show statistics

## Interactive Documentation

When REST API is running:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
