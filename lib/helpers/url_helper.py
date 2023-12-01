import urllib.parse


def parse_url(url: str) -> urllib.parse.ParseResult:
    return urllib.parse.urlparse(url)


def quote_url(url: str, plus=True) -> str:
    if plus:
        return urllib.parse.quote_plus(url)
    else:
        return urllib.parse.quote(url)


def get_url_without_query_params(url: str) -> str:
    parsed_url = parse_url(url)
    return f'{parsed_url.netloc}{parsed_url.path}'


def unquote_url(url: str, plus=True) -> str:
    if plus:
        return urllib.parse.unquote_plus(url)
    else:
        return urllib.parse.unquote(url)


def parse_query_params(query_params: dict[str, ...]) -> str:
    return urllib.parse.urlencode(query_params)


def get_query_param(url: str, param: str) -> list[str]:
    return urllib.parse.parse_qs(parse_url(url).query)[param]


def join_url(base_url: str, path: str, query_params: dict[str, ...]) -> str:
    joined_url = urllib.parse.urljoin(base_url, path)
    return joined_url if not query_params else f'{joined_url}?{parse_query_params(query_params)}'


def get_region(url: str) -> str:
    parsed_url = urllib.parse.urlsplit(url).netloc.split('.')
    if parsed_url[1].lower() == 'beeline':
        return parsed_url[0]
    else:
        raise Exception('В адресе страницы не содержится информация о регионе!')


def get_domain_without_region(url: str) -> str:
    return '.'.join(urllib.parse.urlsplit(url).netloc.split('.')[-2:])
