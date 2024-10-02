# coding=utf-8
"""本包定义了各个端点的请求和返回模型"""

from pydantic import BaseModel, ConfigDict


class LoosenBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
