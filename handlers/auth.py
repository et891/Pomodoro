from typing import Annotated

from dependecy import get_auth_service
from exeption import UserNotFoundException, UserNotCorrectPasswordException
from schema import UserLoginSchema, UserCreateSchema
from fastapi import APIRouter, Depends, HTTPException

from service import UserService
from service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=UserLoginSchema
)
async def login(
        body: UserCreateSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
