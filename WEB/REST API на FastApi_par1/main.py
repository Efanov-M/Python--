
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

advertisements = {}
next_id = 1


class AdvertisementCreate(BaseModel):
    title: str
    description: str
    price: float = Field(ge=0)
    author: str


class AdvertisementUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, ge=0)
    author: str | None = None


class Advertisement(AdvertisementCreate):
    id: int
    created_at: datetime


@app.post("/advertisement", status_code=201)
def create_advertisement(data: AdvertisementCreate):
    global next_id

    advertisement = Advertisement(
        id=next_id,
        created_at=datetime.now(timezone.utc),
        **data.model_dump()
    )

    advertisements[next_id] = advertisement
    next_id += 1

    return advertisement


@app.patch("/advertisement/{advertisement_id}")
def update_advertisement(
    advertisement_id: int,
    data: AdvertisementUpdate
):
    if advertisement_id not in advertisements:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    updates = data.model_dump(exclude_unset=True)

    if any(value is None for value in updates.values()):
        raise HTTPException(status_code=422, detail="Fields cannot be null")

    advertisement = advertisements[advertisement_id]
    updated = advertisement.model_copy(update=updates)

    advertisements[advertisement_id] = updated

    return updated


@app.delete("/advertisement/{advertisement_id}", status_code=204)
def delete_advertisement(advertisement_id: int):
    if advertisement_id not in advertisements:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    del advertisements[advertisement_id]


@app.get("/advertisement/{advertisement_id}")
def get_advertisement(advertisement_id: int):
    if advertisement_id not in advertisements:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    return advertisements[advertisement_id]


@app.get("/advertisement")
def search_advertisements(
    title: str | None = None,
    description: str | None = None,
    price: float | None = None,
    author: str | None = None,
    created_at: datetime | None = None
):
    results = list(advertisements.values())

    if title is not None:
        results = [
            ad for ad in results
            if title.lower() in ad.title.lower()
        ]

    if description is not None:
        results = [
            ad for ad in results
            if description.lower() in ad.description.lower()
        ]

    if price is not None:
        results = [
            ad for ad in results
            if ad.price == price
        ]

    if author is not None:
        results = [
            ad for ad in results
            if author.lower() in ad.author.lower()
        ]

    if created_at is not None:
        results = [
            ad for ad in results
            if ad.created_at == created_at
        ]

    return results
