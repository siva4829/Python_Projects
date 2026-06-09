from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from model import User,Expense
from schemas import add_expense
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy  import select
from database import get_db
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv("../.env")

router = APIRouter()
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGO")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)

async def get_current_user(token: str = Depends(oauth2_scheme),db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username = payload.get("sub")
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )
        return user

    except JWTError:
        raise HTTPException(status_code=403, detail="JWT error")
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.post("/addExpense")
async def add_expenses(
    addexpense:add_expense,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_expense = Expense(
        expense_item=addexpense.expense_item,
        expense_category=addexpense.expense_category,
        amount=addexpense.amount,
        owner_id=current_user.id,
        expense_date=datetime.utcnow()
    )
    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)
    return new_expense


@router.get("/getExpenses")
async def get_expenses(db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    result=await db.execute(select(Expense).where(Expense.owner_id == current_user.id))
    get_expenses = result.scalars().all()
    return get_expenses

@router.put("/updateExpense/{expense_id}")
async def remove_expense(editexpense:add_expense,expense_id:int,db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Expense).where(
            Expense.id == expense_id,
            Expense.owner_id == current_user.id
        )
    )
    getresult = result.scalar_one_or_none()
    if not getresult:
        raise HTTPException(status_code=404, detail="Expense not found")
    getresult.expense_item = editexpense.expense_item
    getresult.expense_category = editexpense.expense_category
    getresult.amount = editexpense.amount
    await db.commit()
    await db.refresh(getresult)
    return getresult

@router.delete("/removeExpense/{expense_id}")
async def delete_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Expense).where(
            Expense.id == expense_id,
                Expense.owner_id == current_user.id
    )
    )
    getresult = result.scalar_one_or_none()
    if not getresult:
        raise HTTPException(status_code=404, detail="Expense not found")

    await db.delete(getresult)
    await db.commit()

    return {"status": "success"}



