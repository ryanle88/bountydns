from typing import List

from pydantic import BaseModel

from bountydns.core.entities.base.responses import BaseResponse
from bountydns.core.entities.api_token.data import ApiTokenData, SensitiveApiTokenData


class ApiTokenResponse(BaseResponse):
    api_token: ApiTokenData


class ApiTokensResponse(BaseResponse):
    api_tokens: List[ApiTokenData]


class SensitiveApiTokenResponse(BaseResponse):
    api_token: SensitiveApiTokenData
