# lookupCacheAPI
Semi persistant TTL lookup passthrough

```bash
make
curl -X POST -H "Content-Type: application/json" -d '{"id": "Your Todo Title", "payload": {"hello": "world"}, "timestamp": 0}' http://localhost:8000/add
```
