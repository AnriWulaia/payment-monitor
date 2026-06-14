## Live Demo
- Dashboard: https://payment-monitor-anri.streamlit.app
- API docs: https://payment-monitor-production.up.railway.app/docs

# Payment Monitor API

Internal payment monitoring tool built with FastAPI and SQLite. Tracks transactions, calculates stats, and flags suspicious activity. Frontend dashboard built with Streamlit.

## Stack
- FastAPI + SQLite — backend and database
- Streamlit + Plotly — dashboard
- Pandas — data processing

## Setup

```bash
pip install fastapi uvicorn streamlit pandas plotly requests
```

Run the API:
```bash
uvicorn main:app --reload
```

Run the dashboard (separate terminal):
```bash
python3 -m streamlit run dashboard.py
```

API: `http://localhost:8000/docs`  
Dashboard: `http://localhost:8501`

## Endpoints

| Method | Endpoint | Description |
| GET | `/payments` | All transactions |
| GET | `/payments/{id}` | Single transaction |
| GET | `/payments/stats` | Volume, average, success rate |
| GET | `/payments/suspicious` | Transactions over $10,000 |
| POST | `/payments` | Add a transaction |
