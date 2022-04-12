from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
import os
from dotenv import load_dotenv
from starlette.requests import Request
import time
import requests

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']

)

# This should be a different database
redis = get_redis_connection(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    password=os.getenv('REDIS_PASSWORD'),
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)


@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks):  # id, quantity
    body = await request.json()

    req = request.get('http://localhost:8000/products/%s' % body['id'])

    product = req.json()
    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=product['price'] * 0.2,
        total=product['price'] * 1.2,
        quantity=body['quantity'],
        status='pending'  # default status is pending
    )
    order.save()

    background_tasks.add_task(order_completed, order)

    return order


def order_completed(order: Order):  # Update the order status
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')  # * is for random generated id
