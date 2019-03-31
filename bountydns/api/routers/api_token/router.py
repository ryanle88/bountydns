from fastapi import APIRouter, Depends, HTTPException
from bountydns.core import logger, only
from bountydns.core.security import ScopedTo, TokenPayload
from bountydns.core.entities import (
    PaginationQS,
    ApiTokensResponse,
    ApiTokenResponse,
    ApiTokenRepo,
    ApiTokenCreateForm,
    BaseResponse,
)
import uuid


router = APIRouter()
options = {"prefix": ""}


@router.get("/api-token", name="api_token.index", response_model=ApiTokensResponse)
async def index(
    pagination: PaginationQS = Depends(PaginationQS),
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo),
    token: TokenPayload = ScopedTo("api-token:list"),
):
    pg, items = api_token_repo.paginate(pagination).data()
    return ApiTokensResponse(pagination=pg, api_tokens=items)


@router.post("/api-token", name="api_token.store", response_model=ApiTokenResponse)
async def index(
    form: ApiTokenCreateForm,
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo),
    token: TokenPayload = ScopedTo("api-token:create"),
):
    scopes = []
    for requested_scope in form.scopes.split(" "):
        request_scope_satisfied = False
        for user_token in token["scopes"]:
            # TODO: double check this, pretty lenient
            # if a:b in a:b:c
            if user_token in requested_scope:
                request_scope_satisfied = True
        if not request_scope_satisfied:
            logger.warning(f"Attempt to create unauthorized scope {requested_scope}")
            raise HTTPException(403, detail="unauthorized")
        else:
            scopes.append(requested_scope)

    # TODO: use better randomness
    data = {
        "scopes": " ".join(scopes),
        "token": uuid.uuid4().hex,
        "expires_at": form.expires_at,
    }
    api_token = api_token_repo.create(data).data()
    return ApiTokenResponse(api_token=api_token)


@router.delete("/api-token/{api_token_id}", response_model=BaseResponse)
async def destroy(
    api_token_id: int,
    api_token_repo: ApiTokenRepo = Depends(ApiTokenRepo),
    token: TokenPayload = ScopedTo("api-token:destroy"),
):
    messages = [{"text": "Deactivation Succesful", "type": "success"}]
    if not api_token_repo.exists(api_token_id):
        return BaseResponse(messages=messages)
    api_token_repo.deactivate(api_token_id)
    return BaseResponse(messages=messages)