from pydantic import BaseModel

class Product(BaseModel):
  id: int
  name: str
  basic_price: int
  product_price: int
  review_rating: int
  feedbacks: int
  quantity: int

  class Config:
    from_attributes=True
