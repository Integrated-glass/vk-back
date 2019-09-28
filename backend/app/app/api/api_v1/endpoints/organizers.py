from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.types import EmailStr
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.core import config
from app.api.utils.security import get_current_user
from app.db_models.models import Organizer as DBUser
from app.models.models import Organizer, OrganizerCreate, Token
from app.core.jwt import create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


# @router.get("/", response_model=List[Organizer])
# def read_users(
#     db: Session = Depends(get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: DBUser = Depends(get_current_active_superuser),
# ):
#     """
#     Retrieve users.
#     """
#     users = crud.organizer.get_multi(db, skip=skip, limit=limit)
#     return users
#
#
# @router.post("/", response_model=Organizer)
# def create_user(
#     *,
#     db: Session = Depends(get_db),
#     user_in: OrganizerCreate,
#     current_user: DBUser = Depends(get_current_active_superuser),
# ):
#     """
#     Create new user.
#     """
#     user = crud.organizer.get_by_email(db, email=user_in.email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this username already exists in the system.",
#         )
#     user = crud.organizer.create(db, user_in=user_in)
#     return user
#

# @router.put("/me", response_model=Organizer)
# def update_user_me(
#     *,
#     db: Session = Depends(get_db),
#     password: str = Body(None),
#     full_name: str = Body(None),
#     email: EmailStr = Body(None),
#     current_user: DBUser = Depends(get_current_user),
# ):
#     """
#     Update own user.
#     """
#     current_user_data = jsonable_encoder(current_user)
#     user_in = OrganizerUpdate(**current_user_data)
#     if password is not None:
#         user_in.password = password
#     if full_name is not None:
#         user_in.full_name = full_name
#     if email is not None:
#         user_in.email = email
#     user = crud.organizer.update(db, user=current_user, user_in=user_in)
#     return user


@router.get("/me", response_model=Organizer)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    """
    Get current user.
    """
    return current_user


@router.post("/register", response_model=Token)
def create_user_open(
    *,
    db: Session = Depends(get_db),
    user_create: OrganizerCreate
):
    """
    Create new user without the need to be logged in.
    """
    if not config.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user resgistration is forbidden on this server",
        )
    user = crud.organizer.get_by_email(db, email=user_create.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = crud.organizer.create(db, user_in=user_create)
    return {
        "access_token": create_access_token(
            data={"user_id": user.id}, expires_delta= ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        "token_type": "bearer"
    }


# @router.get("/{user_id}", response_model=Organizer)
# def read_user_by_id(
#     user_id: int,
#     current_user: DBUser = Depends(get_current_active_user),
#     db: Session = Depends(get_db),
# ):
#     """
#     Get a specific user by id.
#     """
#     user = crud.organizer.get(db, user_id=user_id)
#     if user == current_user:
#         return user
#     if not crud.organizer.is_superuser(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return user
#
#
# @router.put("/{user_id}", response_model=Organizer)
# def update_user(
#     *,
#     db: Session = Depends(get_db),
#     user_id: int,
#     user_in: OrganizerUpdate,
#     current_user: OrganizerInDB = Depends(get_current_active_superuser),
# ):
#     """
#     Update a user.
#     """
#     user = crud.organizer.get(db, user_id=user_id)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system",
#         )
#     user = crud.organizer.update(db, user=user, user_in=user_in)
#     return user
