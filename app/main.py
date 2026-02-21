from fastapi import FastAPI, HTTPException
from . import schemas, services

app = FastAPI(title="BlackRock Auto-Saving Challenge API")

# transaction parse
@app.post("/blackrock/challenge/v1/transactions:parse", response_model=schemas.ParseResponse)
def parse_transactions(transactions: list[schemas.Expense]):
    return services.parse_transactions(transactions)

# transaction validator
@app.post("/blackrock/challenge/v1/transactions:validator", response_model=schemas.ValidationResponse)
def validate_transactions(request: schemas.ValidationRequest):
    return services.validate_transactions(request)

# temporal filter
@app.post("/blackrock/challenge/v1/transactions:filter", response_model=schemas.FilterResponse)
def filter_transactions(request: schemas.FilterRequest):
    return services.filter_transactions(request)

# returns endpoints
@app.post("/blackrock/challenge/v1/returns:nps", response_model=schemas.ReturnsResponse)
def calculate_nps_returns(request: schemas.ReturnsRequest):
    return services.calculate_returns(request, mode="nps")

@app.post("/blackrock/challenge/v1/returns:index", response_model=schemas.ReturnsResponse)
def calculate_index_returns(request: schemas.ReturnsRequest):
    return services.calculate_returns(request, mode="index")

# performance
@app.get("/blackrock/challenge/v1/performance", response_model=schemas.PerformanceResponse)
def performance():
    return services.performance_report()
