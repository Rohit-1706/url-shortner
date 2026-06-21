Building A URL Shortner

- POST /shorten         - {"url": "https://google.com} -> {"code": "aB234"}
- GET /{code}           - 302 redirect to original URL
- GET /stats/{code}     - {"clicks": 42, "url": "..."}

