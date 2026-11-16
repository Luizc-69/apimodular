from fastapi import FastAPI
from app.core.database import criar_tabelas
from app.api.routes import registros

app = FastAPI(
    title="API Modular",
    description="Estrutura modularizada do zero.",
    version="1.0.0"
)


@app.on_event("startup")
def startup_event():
    criar_tabelas()


app.include_router(registros.router)
