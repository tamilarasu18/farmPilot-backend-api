from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select, extract, func
from sqlalchemy.ext.asyncio import AsyncSession
from collections import defaultdict
from calendar import month_name

from app.database import get_db
from app.dependencies import get_current_user
from app.models.daily_log import DailyLog, Expense, Income
from app.models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


class MonthlyFinancials(BaseModel):
    month: str
    month_index: int
    revenue: float
    expenses: float
    profit: float


class AnalyticsResponse(BaseModel):
    total_revenue: float
    total_expenses: float
    net_profit: float
    monthly_data: list[MonthlyFinancials]
    expense_breakdown: dict[str, float]


@router.get("/finance", response_model=AnalyticsResponse)
async def get_financial_analytics(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    year: int | None = None,
):
    """Get financial analytics (revenue, expenses, profit) for a specific year or all time."""
    # 1. Base query for user's logs
    log_query = select(DailyLog.id).where(DailyLog.user_id == current_user.id)
    if year:
        log_query = log_query.where(extract('year', DailyLog.log_date) == year)

    # We need the log IDs to filter expenses and incomes
    log_ids_result = await db.execute(log_query)
    log_ids = [row[0] for row in log_ids_result.all()]

    if not log_ids:
        return AnalyticsResponse(
            total_revenue=0,
            total_expenses=0,
            net_profit=0,
            monthly_data=[],
            expense_breakdown={}
        )

    # 2. Expenses breakdown and monthly sum
    # Join Expense with DailyLog to get the log_date
    expense_query = (
        select(
            Expense.category,
            extract('month', DailyLog.log_date).label('month'),
            func.sum(Expense.amount).label('total')
        )
        .join(DailyLog, Expense.daily_log_id == DailyLog.id)
        .where(Expense.daily_log_id.in_(log_ids))
        .group_by(Expense.category, extract('month', DailyLog.log_date))
    )
    expense_result = await db.execute(expense_query)
    
    expense_breakdown = defaultdict(float)
    monthly_expenses = defaultdict(float)
    total_expenses = 0.0

    for category, month, total in expense_result.all():
        amount = float(total or 0)
        expense_breakdown[category] += amount
        monthly_expenses[int(month)] += amount
        total_expenses += amount

    # 3. Income monthly sum
    income_query = (
        select(
            extract('month', DailyLog.log_date).label('month'),
            func.sum(Income.amount).label('total')
        )
        .join(DailyLog, Income.daily_log_id == DailyLog.id)
        .where(Income.daily_log_id.in_(log_ids))
        .group_by(extract('month', DailyLog.log_date))
    )
    income_result = await db.execute(income_query)

    monthly_revenue = defaultdict(float)
    total_revenue = 0.0

    for month, total in income_result.all():
        amount = float(total or 0)
        monthly_revenue[int(month)] += amount
        total_revenue += amount

    # 4. Build monthly data list
    monthly_data = []
    # If year is specified, show all 12 months. If all time, show months that have data
    months_to_show = range(1, 13) if year else sorted(list(set(monthly_expenses.keys()) | set(monthly_revenue.keys())))

    for m in months_to_show:
        rev = monthly_revenue.get(m, 0.0)
        exp = monthly_expenses.get(m, 0.0)
        monthly_data.append(MonthlyFinancials(
            month=month_name[m][:3], # Jan, Feb, etc.
            month_index=m,
            revenue=rev,
            expenses=exp,
            profit=rev - exp
        ))

    # Sort by month index just in case
    monthly_data.sort(key=lambda x: x.month_index)

    return AnalyticsResponse(
        total_revenue=total_revenue,
        total_expenses=total_expenses,
        net_profit=total_revenue - total_expenses,
        monthly_data=monthly_data,
        expense_breakdown=dict(expense_breakdown)
    )
