from contextlib import asynccontextmanager

from fastapi_mqtt import FastMQTT, MQTTConfig
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Messages
import asyncio
from sqlalchemy.exc import IntegrityError


from sqlalchemy.orm import Session
import ssl
from gmqtt.mqtt.constants import MQTTv311
from .settings import MqttSettings

from .schemas import MessageCreate
from . import crud

mqqt_settings = MqttSettings()

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

fast_mqtt = FastMQTT(config=MQTTConfig(
    host = mqqt_settings.host,  # Změňte na hostitele vašeho MQTT serveru
    port = mqqt_settings.port,  # Změňte na port vašeho MQTT serveru
    keepalive=60,
    version=MQTTv311,
    ssl=ssl_ctx,  # Změňte na True, pokud je vyžadováno šifrování
    username = mqqt_settings.username,  # Přidejte uživatel,ské jméno, pokud je vyžadováno
    password = mqqt_settings.password, 
))

@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    fast_mqtt.client.subscribe("#") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@fast_mqtt.on_message()
async def message(client, topic, payload, qos, properties):    
    pass


@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)
