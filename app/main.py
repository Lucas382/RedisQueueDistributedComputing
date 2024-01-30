"""Main App
    App to push messages into the redis queue
"""
from datetime import datetime
from json import dumps
import random
from time import sleep
from uuid import uuid4
import redis
from decouple import config

def redis_db():
    try:
        db = redis.Redis(
            host=config("REDIS_HOST"),
            port=config("REDIS_PORT", cast=int),
            db=config("REDIS_DB_NUMBER", cast=int),
            password=config("REDIS_PASSWORD"),
            decode_responses=True

        )

    
        db.ping()
        
        return db
    
    except redis.exeptions.RedisError as e:
        print(f"Erro ao conectar ao banco de dados Redis: {e}")
        return None
    

def redis_queue_push(db: redis.Redis, message):
    db.lpush(config("REDIS_QUEUE_NAME"), message)

def main(num_messages: int, delay: float = 1):
    """
    Generates `num_messages` and pushes them to a Redis queue
    :param num_messages:
    :return:
    """

    db = redis_db()

    for i in range(num_messages):
        #Generate message data
        message = {
            "id": str(uuid4()),
            "ts": datetime.utcnow().isoformat(),
            "data": {
                "message_number": i,
                "x": random.randrange(0, 100),
                "y": random.randrange(0, 100),
            },
        }

        message_json = dumps(message)

        print(f"Sending message {i+1} (id={message['id']})")
        redis_queue_push(db, message_json)

        sleep(delay)


if __name__ == "__main__":
    main(num_messages=30, delay= 0.1)