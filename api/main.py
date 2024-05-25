import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models
from .routers import topics, messages

from . import mqtt

models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("api.main:app",
                host="0.0.0.0",
                port=8000,
                reload=True,
    )
    

app = FastAPI(
    debug=True,
    title="API",
    root_path="/",
    redoc_url=None,
    docs_url="/docs",
    )

mqtt.fast_mqtt.init_app(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)


app.include_router(topics.router)
app.include_router(messages.router)
    