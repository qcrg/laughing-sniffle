import tomllib as toml
from pydantic import BaseModel

class Database(BaseModel):
  protocol: str
  user: str
  host: str
  port: int
  name: str
  #FIXME
  password: str

  def get_url(self) -> str:
    return f"{self.protocol}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

class Config(BaseModel):
  database: Database

def load(path: str = "./config.toml") -> Config:
  with open(path, "rb") as f:
    conf = toml.load(f)
    return Config(**conf)

conf: Config = load()
