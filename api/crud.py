from .models import Messages
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from .schemas import Message, MessageStatus

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
    messages = db.query(func.count(Messages.id).label("message_count"),Messages.date.label("date"), func.sum(Messages.size).label('size')).filter(Messages.topic.like(f"{path}%")).filter(Messages.date >= start_date).filter(Messages.date <= end_date).group_by(Messages.date).all()
    
    if not messages:
        return None
    
    mess = []
    
    for row in messages:
        
        mess.append(Message(count=row.message_count, date=row.date, size=row.size))
    
    return mess

def get_message_count(db: Session, path: str, start_date: datetime, end_date: datetime):
    message_count = db.query(Message).filter(Messages.topic.like(f"{path}%")).filter(Messages.date >= start_date).filter(Messages.date <= end_date).count()
    
    return MessageStatus(count=message_count)