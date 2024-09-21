# coding=utf-8
from pydantic import BaseModel, ConfigDict


class LoosenBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
