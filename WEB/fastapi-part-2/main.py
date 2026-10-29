
import hashlib
import hmac
import os
import secrets

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Literal

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field


app = FastAPI(title="Advertisement API")

security = HTTPBearer(auto_error=False)

SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
ALGORITHM = "HS256"
TOKEN_LIFETIME = timedelta(hours=48)

users = {}
advertisements = {}

next_user_id = 1
next_advertisement_id = 1


# ---------- Модели пользователей ----------

class UserCreate(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    group: Literal["user", "admin"] = "user"


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1)
    password: str | None = Field(default=None, min_length=1)
    group: Literal["user", "admin"] | None = None


class LoginData(BaseModel):
    username: str
    password: str


# ---------- Модели объявлений ----------

class AdvertisementCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    price: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    author: str = Field(min_length=1)


class AdvertisementUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=1)
    price: Decimal | None = Field(default=None, ge=0)
    author: str | None = Field(default=None, min_length=1)


# ---------- Работа с паролями ----------

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000,
    )

    return f"{salt.hex()}${password_hash.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    salt_hex, hash_hex = stored_hash.split("$")

    calculated_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        600_000,
    )

    return hmac.compare_digest(
        calculated_hash,
        bytes.fromhex(hash_hex),
    )


# ---------- JWT ----------

def create_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + TOKEN_LIFETIME,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
):
    if credentials is None:
        return None

    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["sub", "exp"]},
        )

        user_id = int(payload["sub"])

    except (jwt.PyJWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    user = users.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid user",
        )

    return user


def require_user(current_user=Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=403,
            detail="Permission denied",
        )

    return current_user


def require_admin(current_user=Depends(require_user)):
    if current_user["group"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Permission denied",
        )

    return current_user


def check_permission(current_user: dict, owner_id: int):
    if current_user["group"] == "admin":
        return

    if current_user["id"] != owner_id:
        raise HTTPException(
            status_code=403,
            detail="Permission denied",
        )


# ---------- Вспомогательные функции ----------

def get_user_or_404(user_id: int) -> dict:
    user = users.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


def get_advertisement_or_404(advertisement_id: int) -> dict:
    advertisement = advertisements.get(advertisement_id)

    if advertisement is None:
        raise HTTPException(
            status_code=404,
            detail="Advertisement not found",
        )

    return advertisement


def public_user(user: dict) -> dict:
    return {
        "id": user["id"],
        "username": user["username"],
        "group": user["group"],
    }


def public_advertisement(advertisement: dict) -> dict:
    return {
        "id": advertisement["id"],
        "title": advertisement["title"],
        "description": advertisement["description"],
        "price": advertisement["price"],
        "author": advertisement["author"],
        "created_at": advertisement["created_at"],
    }


def check_username(
    username: str,
    exclude_id: int | None = None,
):
    for user in users.values():
        if user["username"] == username and user["id"] != exclude_id:
            raise HTTPException(
                status_code=409,
                detail="Username already exists",
            )


def validate_updates(updates: dict):
    if any(value is None for value in updates.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null",
        )


# ---------- Начальный администратор ----------

admin_username = os.getenv("ADMIN_USERNAME")
admin_password = os.getenv("ADMIN_PASSWORD")

if admin_username and admin_password:
    users[next_user_id] = {
        "id": next_user_id,
        "username": admin_username,
        "password_hash": hash_password(admin_password),
        "group": "admin",
    }

    next_user_id += 1


# ---------- Авторизация ----------

@app.post("/login")
def login(data: LoginData):
    for user in users.values():
        if user["username"] == data.username:
            if verify_password(
                data.password,
                user["password_hash"],
            ):
                return {
                    "access_token": create_token(user["id"]),
                    "token_type": "bearer",
                }

    raise HTTPException(
        status_code=401,
        detail="Invalid username or password",
    )


# ---------- Управление пользователями ----------

@app.post("/user", status_code=201)
def create_user(
    data: UserCreate,
    current_user=Depends(get_current_user),
):
    global next_user_id

    if data.group == "admin":
        if current_user is None or current_user["group"] != "admin":
            raise HTTPException(
                status_code=403,
                detail="Permission denied",
            )

    check_username(data.username)

    user = {
        "id": next_user_id,
        "username": data.username,
        "password_hash": hash_password(data.password),
        "group": data.group,
    }

    users[next_user_id] = user
    next_user_id += 1

    return public_user(user)


@app.get("/user")
def get_users(current_user=Depends(require_admin)):
    return [
        public_user(user)
        for user in users.values()
    ]


@app.get("/user/{user_id}")
def get_user(user_id: int):
    user = get_user_or_404(user_id)

    return public_user(user)


@app.patch("/user/{user_id}")
def update_user(
    user_id: int,
    data: UserUpdate,
    current_user=Depends(require_user),
):
    user = get_user_or_404(user_id)

    check_permission(current_user, user_id)

    updates = data.model_dump(exclude_unset=True)
    validate_updates(updates)

    if "group" in updates and current_user["group"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Permission denied",
        )

    if "username" in updates:
        check_username(
            updates["username"],
            exclude_id=user_id,
        )

        old_username = user["username"]
        new_username = updates["username"]

        user["username"] = new_username

        # Обновляем автора существующих объявлений пользователя.
        for advertisement in advertisements.values():
            if advertisement["owner_id"] == user_id:
                if advertisement["author"] == old_username:
                    advertisement["author"] = new_username

    if "password" in updates:
        user["password_hash"] = hash_password(
            updates["password"]
        )

    if "group" in updates:
        user["group"] = updates["group"]

    return public_user(user)


@app.delete("/user/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    current_user=Depends(require_user),
):
    get_user_or_404(user_id)

    check_permission(current_user, user_id)

    # Удаляем объявления вместе с учётной записью владельца.
    advertisement_ids = [
        ad_id
        for ad_id, advertisement in advertisements.items()
        if advertisement["owner_id"] == user_id
    ]

    for advertisement_id in advertisement_ids:
        del advertisements[advertisement_id]

    del users[user_id]


# ---------- Управление объявлениями ----------

@app.post("/advertisement", status_code=201)
def create_advertisement(
    data: AdvertisementCreate,
    current_user=Depends(require_user),
):
    global next_advertisement_id

    if (
        current_user["group"] != "admin"
        and data.author != current_user["username"]
    ):
        raise HTTPException(
            status_code=403,
            detail="Author must match current user",
        )

    advertisement = {
        "id": next_advertisement_id,
        **data.model_dump(),
        "owner_id": current_user["id"],
        "created_at": datetime.now(timezone.utc),
    }

    advertisements[next_advertisement_id] = advertisement
    next_advertisement_id += 1

    return public_advertisement(advertisement)


@app.get("/advertisement/{advertisement_id}")
def get_advertisement(advertisement_id: int):
    advertisement = get_advertisement_or_404(
        advertisement_id
    )

    return public_advertisement(advertisement)


@app.patch("/advertisement/{advertisement_id}")
def update_advertisement(
    advertisement_id: int,
    data: AdvertisementUpdate,
    current_user=Depends(require_user),
):
    advertisement = get_advertisement_or_404(
        advertisement_id
    )

    check_permission(
        current_user,
        advertisement["owner_id"],
    )

    updates = data.model_dump(exclude_unset=True)
    validate_updates(updates)

    if (
        "author" in updates
        and current_user["group"] != "admin"
        and updates["author"] != current_user["username"]
    ):
        raise HTTPException(
            status_code=403,
            detail="Author must match current user",
        )

    advertisement.update(updates)

    return public_advertisement(advertisement)


@app.delete("/advertisement/{advertisement_id}", status_code=204)
def delete_advertisement(
    advertisement_id: int,
    current_user=Depends(require_user),
):
    advertisement = get_advertisement_or_404(
        advertisement_id
    )

    check_permission(
        current_user,
        advertisement["owner_id"],
    )

    del advertisements[advertisement_id]


@app.get("/advertisement")
def search_advertisements(
    title: str | None = None,
    description: str | None = None,
    price: Decimal | None = None,
    author: str | None = None,
    created_at: datetime | None = None,
):
    results = list(advertisements.values())

    if title is not None:
        results = [
            ad for ad in results
            if title.lower() in ad["title"].lower()
        ]

    if description is not None:
        results = [
            ad for ad in results
            if description.lower() in ad["description"].lower()
        ]

    if price is not None:
        results = [
            ad for ad in results
            if ad["price"] == price
        ]

    if author is not None:
        results = [
            ad for ad in results
            if author.lower() in ad["author"].lower()
        ]

    if created_at is not None:
        results = [
            ad for ad in results
            if ad["created_at"] == created_at
        ]

    return [
        public_advertisement(ad)
        for ad in results
    ]
