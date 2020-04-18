def init_routes(parent, routes):
    for _route in routes:
        parent.include_router(
            _route[0], **_route[1]
        )
