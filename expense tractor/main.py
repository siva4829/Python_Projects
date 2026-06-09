from fastapi import FastAPI

from database import engine, Base

from route import user, expense


app = FastAPI()


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )


app.include_router(user.router)

app.include_router(expense.router)