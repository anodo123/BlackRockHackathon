from datetime import datetime
from . import schemas
from typing import List
import time
import threading
import psutil

def parse_transactions(expenses: List[schemas.Expense]) -> schemas.ParseResponse:
    transactions: List[schemas.Transaction] = []
    total_amount = 0.0
    total_ceiling = 0.0
    total_remanent = 0.0
    for e in expenses:
        ceiling = ((int(e.amount) + 99) // 100) * 100
        remanent = ceiling - e.amount
        t = schemas.Transaction(date=e.date, amount=e.amount, ceiling=ceiling, remanent=remanent)
        transactions.append(t)
        total_amount += e.amount
        total_ceiling += ceiling
        total_remanent += remanent
    return schemas.ParseResponse(
        transactions=transactions,
        total_amount=total_amount,
        total_ceiling=total_ceiling,
        total_remanent=total_remanent,
    )


def validate_transactions(request: schemas.ValidationRequest) -> schemas.ValidationResponse:
    valid: List[schemas.Transaction] = []
    invalid: List[schemas.InvalidTransaction] = []
    seen = set()
    for t in request.transactions:
        msg = None
        # amount must be nonnegative and not greater than wage maybe? unclear.
        if t.amount < 0:
            msg = "negative amount"
        # duplicates by date+amount
        key = (t.date, t.amount)
        if key in seen:
            msg = "duplicate"
        seen.add(key)
        if msg:
            invalid.append(schemas.InvalidTransaction(**t.dict(), message=msg))
        else:
            valid.append(t)
    return schemas.ValidationResponse(valid=valid, invalid=invalid)


def filter_transactions(request: schemas.FilterRequest) -> schemas.FilterResponse:
    valid: List[schemas.Transaction] = []
    invalid: List[schemas.InvalidTransaction] = []
    for t in request.transactions:
        msg = None
        if t.amount < 0:
            msg = "negative amount"
        if msg:
            invalid.append(schemas.InvalidTransaction(**t.dict(), message=msg))
            continue
        # apply q/p modifications
        rem = t.remanent
        # find applicable q
        applicable_q = None
        for period in request.q:
            if period.start <= t.date <= period.end:
                if not applicable_q or period.start > applicable_q.start:
                    applicable_q = period
        if applicable_q:
            rem = applicable_q.fixed
        # apply p additions
        for period in request.p:
            if period.start <= t.date <= period.end:
                rem += period.extra
        # replace remanent
        data = t.model_dump() if hasattr(t, 'model_dump') else t.dict()
        data['remanent'] = rem
        t2 = schemas.Transaction(**data)
        valid.append(t2)
    return schemas.FilterResponse(valid=valid, invalid=invalid)


def calculate_returns(request: schemas.ReturnsRequest, mode: str) -> schemas.ReturnsResponse:
    # first parse transactions to calculate ceiling/remanent
    parsed = parse_transactions([schemas.Expense(date=t.date, amount=t.amount) for t in request.transactions])
    # then apply q/p modifications
    filtered_resp = filter_transactions(schemas.FilterRequest(
        q=request.q, p=request.p, k=request.k, wage=request.wage, transactions=parsed.transactions
    ))
    valid = filtered_resp.valid
    total_amount = sum(t.amount for t in valid)
    total_ceiling = sum(t.ceiling for t in valid)

    # compute savings by k periods
    savings_list: List[schemas.SavingsByDate] = []
    for period in request.k:
        amt = 0.0
        # find transactions in period
        for t in valid:
            if period.start <= t.date <= period.end:
                amt += t.remanent
        savings_list.append(schemas.SavingsByDate(start=period.start, end=period.end, amount=amt))
    # compute returns/profits per savings
    for s in savings_list:
        t_years = max(0, 60 - request.age)
        if mode == "nps":
            rate = 0.0711
        else:
            rate = 0.1449
        final = s.amount * ((1 + rate) ** t_years)
        inflation_adj = final / ((1 + request.inflation/100) ** t_years)
        profit = inflation_adj - s.amount
        s.profits = round(profit, 2)
        if mode == "nps":
            # compute tax benefit
            annual_income = request.wage * 12
            deduction = min(s.amount, 0.1 * annual_income, 200000)
            def tax(income):
                slabs = [(700000,0),(1000000,0.1),(1200000,0.15),(1500000,0.2),(float('inf'),0.3)]
                taxamt = 0.0
                prev = 0
                for limit, rate_s in slabs:
                    if income > limit:
                        taxamt += (limit - prev) * rate_s
                        prev = limit
                    else:
                        taxamt += (income - prev) * rate_s
                        break
                return taxamt
            tb = tax(annual_income) - tax(annual_income - deduction)
            s.taxBenefit = round(tb, 2)
    return schemas.ReturnsResponse(
        transactionsTotalAmount=total_amount,
        transactionsTotalCeiling=total_ceiling,
        savingsByDates=savings_list,
    )


def performance_report() -> schemas.PerformanceResponse:
    # simple metrics using psutil
    process = psutil.Process()
    mem = process.memory_info().rss / (1024 * 1024)
    return schemas.PerformanceResponse(
        time="0ms",
        memory=f"{mem:.2f} MB",
        threads=process.num_threads(),
    )
