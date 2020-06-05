from postkit._route import Route


def test_route():
    route = Route(
        method='GET',
        url='http://localhost',
        path='some/{match}/path',
        match={'match': 123},
        query={'query': 'it`s query', 'A': 'B'}
    )

    assert route.furl().tostr() == 'http://localhost/some/123/path?query=it%60s+query&A=B'
