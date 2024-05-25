
from fastapi_mqtt import FastMQTT, MQTTConfig
from sqlalchemy.exc import IntegrityError
import asyncio

import ssl
from gmqtt.mqtt.constants import MQTTv311
from .settings import MqttSettings

from . import crud
from .database import get_session
from .models import Messages

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
    session = get_session()
    try:
        # Create a new message instance        
        message = Messages(
            size=len(payload),
            topic=topic
        )
        session.add(message)
        session.commit()
        # print(f"Message added to DB: {message}")
    except Exception as e:
        session.rollback()
        print(f"Failed to add message to DB: {e}")
    finally:
        session.close()

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)
