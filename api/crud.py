from sqlalchemy.orm import Session

"""
def create_topic(db: Session, topic: Topic):
    db_topic = Topics(name=topic.name, level=topic.level, parent_id=topic.parent_id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

    """