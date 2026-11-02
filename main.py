from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

expenses = []
next_id = 1

class ExpenseCreate(BaseModel):
    title: str
    amount: int = Field(gt=0)
    category: str = "Khac"

class ExpenseUpdate(BaseModel):
    amount: int =  Field(gt=0)

@app.post("/expenses", status_code=201)
def create_expense(data: ExpenseCreate):
    global next_id

    expense = data.model_dump()
    expense["id"] = next_id
    expenses.append(expense)
    next_id += 1
    return expense

@app.get("/expenses")
def get_expenses():
    return {"expenses": expenses}

@app.patch("/expenses/{expense_id}")
def update_expense(expense_id: int, data: ExpenseUpdate):
    for expense in expenses:
        if expense["id"] == expense_id:
            expense["amount"] = data.amount
            return expense
    raise HTTPException(status_code=404, detail="Khong tim thay")

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            expenses.pop(index)
            return {"message": "Xoa thanh cong"}
    raise HTTPException(status_code=404)
