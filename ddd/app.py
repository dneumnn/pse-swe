from typing import Union
from datetime import date
import logging

from fastapi import FastAPI
from fastapi import Request

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import config
import model
import orm
import repository
import services

__NAME = "PSE-SWE Test Application"

LOG = logging.getLogger(__name__)

engine = create_engine(config.URI, echo=True)
orm.mapper_registry.metadata.create_all(engine)
session = Session(engine)
# generate some batches
repository.SqlAlchemyRepository(session).add(model.Batch("4710", "AAA", 100, date(2025,6,30)))
repository.SqlAlchemyRepository(session).add(model.Batch("4711", "AAA", 100, date(2025,12,31)))
repository.SqlAlchemyRepository(session).add(model.Batch("4712", "BBB", 100, date(2025,6,30)))
session.commit()

LOG.info("API starting...")
app = FastAPI()

'''
@app.post("/allocate")
async def allocate(request: Request):
    """allocates an order_line to batches"""
    LOG.info(request)
    batches = repository.SqlAlchemyRepository(session).list()
    _json = await request.json()
    orderid = _json["orderid"]
    sku = _json["sku"]
    qty = _json["qty"]

    line = model.OrderLine(orderid,
                           sku,
                           qty)
    
    batchref = model.allocate(line, batches)

    return {"batchref": batchref}
'''
# REFACTORING
from pydantic import BaseModel
class DTO_OrderLine(BaseModel):
    orderid: str
    sku: str
    qty: int

@app.post("/allocate")
async def allocate(order_line: DTO_OrderLine):
    """allocates an order_line to batches"""
    LOG.info(order_line)

    line = model.OrderLine(order_line.orderid,
                           order_line.sku,
                           order_line.qty)

    try:
        batchref = services.allocate(line, repository.SqlAlchemyRepository(session), session)
    except (services.InvalidSku, model.OutOfStock) as e:
        return {"message": str(e)}, 400
    
    return {"batchref": batchref}, 200

@app.post('/test')
async def test(request: Request):
    """returns the request json body"""
    return await request.json()


@app.get("/")
async def router_name() -> str:
    return __NAME

if __name__ == "__main__":
    import os
    import uvicorn
    port = os.environ.get("PORT", 8000)
    uvicorn.run(app, port=port)

