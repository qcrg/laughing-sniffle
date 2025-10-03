#!/bin/env python3

from sqlalchemy.exc import IntegrityError
import model
from pydantic import BaseModel
from typing import Any, List
import requests
import re

class Price(BaseModel):
  basic: int
  product: int

  class Config:
    extra = "ignore"

class Size(BaseModel):
  price: Price

  class Config:
    extra = "ignore"

class Product(BaseModel):
  id: int
  name: str
  reviewRating: float
  feedbacks: int
  totalQuantity: int
  sizes: List[Size]

  class Config:
    extra = "ignore"

class Resp(BaseModel):
  metadata: Any
  products: List[Product]
  total: int

class Err(BaseModel):
  error: str
  code: int

QUERY = "термопаста"
ENDPOINT = "https://u-search.wb.ru/exactmatch/ru/common/v18/search"
tp_match = re.compile(f".*{QUERY}.*", re.IGNORECASE)

def load_data():
  params = {
    "ab_testid": "no_promo",
    "appType": 2,
    "curr": "rub",
    "dest": -1257786,
    "inheritFilters": False,
    "lang": "ru",
    "query": QUERY,
    "resultset": "catalog",
    "suppressSpellcheck": True,
    "page": 1
  }

  with model.session() as session:
    while True:
    # for i in range(1):
      rgresp = requests.get(ENDPOINT, params=params)
      if not rgresp.ok:
        raise RuntimeError(
          f"Data collection error: code={rgresp.status_code} "
          f"reason={rgresp.reason} "
          f"data={rgresp.text}"
        )
      if not "statuscode" in rgresp.headers:
        continue

      if int(rgresp.headers["statuscode"]) != 200:
        err = Err(**rgresp.json())
        if err.error == "page param malformed":
          break
        raise RuntimeError(f"Request error: {rgresp.text}")

      resp = Resp(**rgresp.json())
      if len(resp.products) == 0:
        break

      for raw_prdct in resp.products:
        if len(raw_prdct.sizes) == 0:
          continue
        if len(raw_prdct.sizes) > 1:
          raise NotImplementedError("Sizes of product is greater than 1")
        if not tp_match.search(raw_prdct.name):
          continue
        prdct = model.Product(
          id=int(raw_prdct.id),
          name=str(raw_prdct.name),
          basic_price=int(raw_prdct.sizes[0].price.basic),
          product_price=int(raw_prdct.sizes[0].price.product),
          review_rating=int(raw_prdct.reviewRating * 10),
          feedbacks=int(raw_prdct.feedbacks),
          quantity=int(raw_prdct.totalQuantity)
        )

        try:
          session.add(prdct)
          session.commit()
        except IntegrityError:
          session.rollback()

      params["page"] += 1


if __name__ == "__main__":
  load_data()
else:
  raise Exception("Must be __main__")
