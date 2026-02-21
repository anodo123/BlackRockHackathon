from __future__ import annotations
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class Expense(BaseModel):
    date: datetime
    amount: float


class Transaction(Expense):
    ceiling: float
    remanent: float


class InvalidTransaction(Transaction):
    message: str


class ParseResponse(BaseModel):
    transactions: List[Transaction]
    total_amount: float
    total_ceiling: float
    total_remanent: float


class ValidationRequest(BaseModel):
    wage: float
    transactions: List[Transaction]


class ValidationResponse(BaseModel):
    valid: List[Transaction]
    invalid: List[InvalidTransaction]


class PeriodQ(BaseModel):
    fixed: float
    start: datetime
    end: datetime


class PeriodP(BaseModel):
    extra: float
    start: datetime
    end: datetime


class PeriodK(BaseModel):
    start: datetime
    end: datetime


class FilterRequest(BaseModel):
    q: List[PeriodQ] = Field(default_factory=list)
    p: List[PeriodP] = Field(default_factory=list)
    k: List[PeriodK] = Field(default_factory=list)
    wage: float
    transactions: List[Transaction]


class FilterResponse(BaseModel):
    valid: List[Transaction]
    invalid: List[InvalidTransaction]


class SavingsByDate(BaseModel):
    start: datetime
    end: datetime
    amount: float
    profits: Optional[float] = None
    taxBenefit: Optional[float] = None


class ReturnsRequest(BaseModel):
    age: int
    wage: float
    inflation: float
    q: List[PeriodQ] = Field(default_factory=list)
    p: List[PeriodP] = Field(default_factory=list)
    k: List[PeriodK] = Field(default_factory=list)
    transactions: List[Expense]


class ReturnsResponse(BaseModel):
    transactionsTotalAmount: float
    transactionsTotalCeiling: float
    savingsByDates: List[SavingsByDate]


class PerformanceResponse(BaseModel):
    time: str
    memory: str
    threads: int
