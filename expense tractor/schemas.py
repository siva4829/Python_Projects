from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    password: str
    email: str

class Login_User(BaseModel):
    username: str
    password: str

class add_expense(BaseModel):
    expense_item: str
    expense_category: str
    amount: float

class remove_expense(BaseModel):
    expense_id: int
