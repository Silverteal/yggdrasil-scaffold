# coding=utf-8

from pydantic import BaseModel, ConfigDict


class AppResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
