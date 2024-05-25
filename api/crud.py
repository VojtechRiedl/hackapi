from .models import Messages
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from .schemas import Message, MessageStatus
from .mqtt import fast_mqtt
import random
import json
import time
import paho.mqtt.client as mqtt
from .settings import MqttSettings
import ssl



def get_topics(db: Session, topic: str):
    
    topics = db.query(Messages.topic).filter(Messages.topic.like(f"{topic}%")).distinct().all()
    
    if not topics:
        return None
    
    unique_topics = []
    
    for t in topics:
        c = topic.count('/') #/
        split_topic = t.topic.split("/")[1:]
        
        #print(split_topic)
        #print(c)
        
        if not split_topic[c - 1] in unique_topics:
            unique_topics.append(split_topic[c - 1])
        
    return unique_topics    

def get_messages(db: Session, path: str, start_date: datetime, end_date: datetime):
    #messages = db.query(func.count(Messages.id).label("message_count"),Messages.date.label("date"), func.sum(Messages.size).label('size')).filter(Messages.topic.like(f"{path}%")).filter(Messages.date >= start_date).filter(Messages.date <= end_date).group_by(Messages.date).all()
    
    
    # Build and execute the query
    messages = db.query(
    func.count(Messages.id).label("message_count"),
    func.DATE_FORMAT(Messages.date, '%Y-%m-%d %H:%i:00').label("date"),
    func.sum(Messages.size).label('size')
    ).filter(Messages.topic.like(f"{path}%")).filter(
        Messages.date >= start_date).filter(
        Messages.date <= end_date).group_by(
        func.DATE_FORMAT(Messages.date, '%Y-%m-%d %H:%i:00')
    ).all()    
    
    if len(messages) == 0:
        print("No messages found")
        return None
    
    mess = []
    
    for row in messages:
        
        mess.append(Message(count=row.message_count, date=row.date, size=row.size))
    
    return mess

def get_message_status(db: Session, path: str, start_date: datetime, end_date: datetime):
    message_count_total = db.query(Messages.id).filter(Messages.topic.like(f"{path}%")).filter(Messages.date >= start_date).filter(Messages.date <= end_date).count()
    
    if not message_count_total:
        return None
    message_size = db.query(func.sum(Messages.size).label("size")).filter(Messages.topic.like(f"{path}%")).filter(Messages.date >= start_date).filter(Messages.date <= end_date).scalar()
    
    if not message_size:
        return None
    
    return MessageStatus(count=message_count_total, size=message_size)

def get_sorted_message_size(db: Session, start_date: datetime, end_date: datetime):
    
    sorted = {}
    
    sorted_messages_size = db.query(Messages.topic,func.sum(Messages.size).label("size")).filter(Messages.date >= start_date).filter(Messages.date <= end_date).group_by(Messages.topic).order_by(Messages.size.desc()).all()
    
    for row in sorted_messages_size:
        
        topic = row.topic.split("/")[1]
        
        if topic in sorted:
            sorted[topic] += row.size
        else:
            sorted[topic] = row.size
            
    return sorted   
    
def get_sorted_message_count(db: Session, start_date: datetime, end_date: datetime):
    sorted = {}
    
    sorted_messages_count = db.query(Messages.topic,func.count(Messages.id).label("id")).filter(Messages.date >= start_date).filter(Messages.date <= end_date).group_by(Messages.topic).all()
    
    for row in sorted_messages_count:
        
        topic = row.topic.split("/")[1]
        
        if topic in sorted:
            sorted[topic] += row.id
        else:
            sorted[topic] = row.id
            
    return sorted   
    
def simulate_messages(count: int):


# Function to publish messages

    #"lat", "lon"
    cities = {"prague" : ["50.0875", "14.4214"],
              "brno" : ["49.1925", "16.6083"],
              "ostrava" : ["49.8356", "18.2925"],
              "plzen" : ["49.7475", "13.3775"],
              "liberec" : ["50.7667", "15.0667"],
              "olomouc" : ["49.5939", "17.2508"],
              "budejovice" : ["48.9747", "14.4747"],
              "hradec" : ["50.2092", "15.8322"],
              "pardubice" : ["50.0386", "15.7792"],
              "usti" : ["50.6583", "14.0417"],
              "zlin" : ["49.2331", "17.6669"],
              "jihlava" : ["49.4003", "18.4228"],
              }
    
    
    for i in range(count):
        city_name = random.choice(list(cities.keys()))
        lat, lon = cities[city_name]
        payload = {
            "name": city_name.capitalize(),
            "latitude": float(lat),
            "longitude": float(lon)
        }
        #client.publish(f"/hackithon/{city_name}", json.dumps(payload))        
        time.sleep(1)
    
    #client.disconnect()

    return {"status": "success"}