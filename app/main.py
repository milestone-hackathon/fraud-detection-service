from fastapi import FastAPI

app = FastAPI(title="Fraud Detection Service", version="1.0.0")

from app.api import routes_scoring, routes_rules, routes_lists
app.include_router(routes_scoring.router, prefix="/v1/fraud")
app.include_router(routes_rules.router, prefix="/v1/fraud")
app.include_router(routes_lists.router, prefix="/v1/fraud")

@app.get("/health")
async def health():
    return {"status": "ok"}
