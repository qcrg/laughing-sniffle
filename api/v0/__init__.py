from fastapi import APIRouter
from schemas import Product
from typing import List, Optional
import model

def init(router: APIRouter):
  @router.get("/products", response_model=List[Product])
  async def get_products(query: Optional[str] = None):
    session = model.session()
    res: List[Product] = list()
    dbquery = None
    if query == None:
      dbquery = session.query(model.Product)
    else:
      dbquery = session.query(model.Product)
      dbquery = dbquery.filter(model.Product.name.ilike(f"%{query}%"))

    for prd in dbquery.all():
      res.append(Product.model_validate(prd))
    return res
