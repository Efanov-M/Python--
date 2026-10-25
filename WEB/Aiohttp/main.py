
from datetime import datetime, timezone

from aiohttp import web


routes = web.RouteTableDef()

advertisements = {}
next_id = 1


@routes.post("/advertisement")
async def create_advertisement(request):
    global next_id

    try:
        data = await request.json()
    except (ValueError, web.HTTPBadRequest):
        raise web.HTTPBadRequest(text="Invalid JSON")

    if not isinstance(data, dict):
        raise web.HTTPBadRequest(text="JSON object expected")

    required_fields = ("title", "description", "owner")

    for field in required_fields:
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise web.HTTPBadRequest(text=f"Invalid field: {field}")

    advertisement = {
        "id": next_id,
        "title": data["title"],
        "description": data["description"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner": data["owner"]
    }

    advertisements[next_id] = advertisement
    next_id += 1

    return web.json_response(advertisement, status=201)


@routes.get("/advertisement/{advertisement_id}")
async def get_advertisement(request):
    advertisement_id = int(request.match_info["advertisement_id"])

    advertisement = advertisements.get(advertisement_id)

    if advertisement is None:
        raise web.HTTPNotFound(text="Advertisement not found")

    return web.json_response(advertisement)


@routes.patch("/advertisement/{advertisement_id}")
async def update_advertisement(request):
    advertisement_id = int(request.match_info["advertisement_id"])

    advertisement = advertisements.get(advertisement_id)

    if advertisement is None:
        raise web.HTTPNotFound(text="Advertisement not found")

    try:
        data = await request.json()
    except (ValueError, web.HTTPBadRequest):
        raise web.HTTPBadRequest(text="Invalid JSON")

    if not isinstance(data, dict):
        raise web.HTTPBadRequest(text="JSON object expected")

    allowed_fields = ("title", "description", "owner")

    for field, value in data.items():
        if field not in allowed_fields:
            raise web.HTTPBadRequest(text=f"Unknown field: {field}")

        if not isinstance(value, str) or not value.strip():
            raise web.HTTPBadRequest(text=f"Invalid field: {field}")

    advertisement.update(data)

    return web.json_response(advertisement)


@routes.delete("/advertisement/{advertisement_id}")
async def delete_advertisement(request):
    advertisement_id = int(request.match_info["advertisement_id"])

    if advertisement_id not in advertisements:
        raise web.HTTPNotFound(text="Advertisement not found")

    del advertisements[advertisement_id]

    return web.Response(status=204)


app = web.Application()
app.add_routes(routes)


if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
