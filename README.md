# BlackRock Hackathon Challenge

This repository implements the auto-saving retirement API using FastAPI.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn app.main:app --reload --port 5477
   ```

3. API documentation available at `http://localhost:5477/docs`.

## Docker

Build and run with:

```bash
docker build -t blk-hacking-ind-yourname .
docker run -d -p 5477:5477 blk-hacking-ind-yourname
```

## Tests

Execute tests using pytest:

```bash
pytest test/test_api.py
```

## Endpoints

- `/blackrock/challenge/v1/transactions:parse` POST
- `/blackrock/challenge/v1/transactions:validator` POST
- `/blackrock/challenge/v1/transactions:filter` POST
- `/blackrock/challenge/v1/returns:nps` POST
- `/blackrock/challenge/v1/returns:index` POST
- `/blackrock/challenge/v1/performance` GET

See the problem description for details on request/response formats.

## Notes

- Timestamp format: `YYYY-MM-DD HH:mm:ss`.
- This implementation uses simple iteration; performance can be improved if needed.

Good luck!  
