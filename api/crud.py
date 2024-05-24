from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import MessageCreate
from .models import Messages


async def create_message(db: AsyncSession , message: MessageCreate):
    db_message = Messages(topic=message.topic, size=message.size)
    
    await db.add(db_message)
    await db.commit()
    
    return db_message

"""
def create_topic(db: Session, topic: Topic):
    db_topic = Topics(name=topic.name, level=topic.level, parent_id=topic.parent_id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

    """