"""Main worker app

This app listens messages into the redis queue
"""

from json import loads
import random
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


def redis_queue_pop(db: redis.Redis):
    #pop from head of the queue (right of the list)
    #the `b` in `brpop` indicates this is a blocking call (waits until an item becomes avaliable)
    _, message_json = db.brpop(config("REDIS_QUEUE_NAME"))
    return message_json

def process_message(db: redis.Redis, message_json: str):
    message = loads(message_json)
    print(f"Message received: id={message['id']}, message_number={message['data']['message_number']}, message_y={message['data']['y']}, message_x={message['data']['x']}")

    processed_ok = random.choices((True, False), weights=(5, 1), k=1)[0]

    if processed_ok:
        print(f"\tProcessed successfully!")
    else:
        print(f"\tProcessed failed - requeuing...")
        redis_queue_push(db, message_json)

def main():
    """
    Consumes items from the redis queue
    """
    db = redis_db()

    while True:
        message_json = redis_queue_pop(db)
        process_message(db, message_json)


if __name__ == "__main__":
    main()