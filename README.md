# URL Shortener Service

## Approach & Tech Stack

- **Python 3.8+**
- **Flask** for REST API
- **In-memory storage** (thread-safe with threading.Lock)
- **Pytest** for automated tests
- **Dataclasses** for URL mapping


## Features

- Shorten URLs (`POST /api/shorten`)
- Redirect to original URL (`GET /<short_code>`)
- Get analytics (`GET /api/stats/<short_code>`)
- All endpoints return JSON responses
- Error handling for invalid input and unknown codes

## Running the Application

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the server:**
   ```bash
   python -m flask --app app.main run
   ```
   The API will be available at http://localhost:5000
3. **Run tests:**
   ```bash
   pytest / python -m pytest
   # If 'pytest' is not recognized, use:
   python -m pytest
   ```
<!-- 
## Example Usage

**Shorten a URL:**

```bash
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'
```

**Redirect:**

```bash
curl -L http://localhost:5000/abc123
```

**Get analytics:**

```bash
curl http://localhost:5000/api/stats/abc123
``` -->

## AI Usage

ChatGPT  for generating some test cases int test file

## Submission

1. Ensure all tests pass
2. Zip your solution
3. (Optional) Add notes about your approach
4. Share the repository link as instructed

   ```

   ```
