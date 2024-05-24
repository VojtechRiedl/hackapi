import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models
from .routers import topics

models.Base.metadata.create_all(bind=engine)

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_mqtt.config import MQTTConfig
from fastapi_mqtt.fastmqtt import FastMQTT

if __name__ == "__main__":
    uvicorn.run("api.main:app",
                host="0.0.0.0",
                port=8000,
                reload=True,
    )

fast_mqtt = FastMQTT(config=MQTTConfig(
    host = "mqtt.portabo.cz",  # Změňte na hostitele vašeho MQTT serveru
    port = 8883,
    username = "hackithon",  # Přidejte uživatel,ské jméno, pokud je vyžadováno
    password = "zuk8uy9aZXU2wM9trqqA", 
))

@asynccontextmanager
async def _lifespan(_app: FastAPI):
    await fast_mqtt.mqtt_startup()
    yield
    await fast_mqtt.mqtt_shutdown()

app = FastAPI(
    lifespan=_lifespan,
    debug=True,
    title="API",
    root_path="/",
    redoc_url=None,
    docs_url="/docs",)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)


app.include_router(topics.router)
    