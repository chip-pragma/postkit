from postkit._route import Route


def json_handler(route: Route) -> Route:
    if route.json is not None:
        route.headers.update({'Content-Type': 'application/json'})

    return route
