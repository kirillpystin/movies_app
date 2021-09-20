import os

from aiofile import async_open
from aiohttp.web import HTTPException, json_response, middleware
from http import HTTPStatus

@middleware
async def error_middleware(request, handler):
    """Обработчик ошибок.

    Args:
        request: Запрос.
        handler: Обработчик конкретного запроса.

    Returns:
        Response: Ответ.
    """
    try:
        if hasattr(request.match_info._route, 'status') and request.match_info._route.status == 404:
            return json_response({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

        response = await handler(request)

        if isinstance(response, dict) or isinstance(response, list):
            return json_response(response)
        else:
            return response
    except HTTPException as ex:
        if ex.status != 404:
            raise
        message = ex.reason
    return json_response({"error": message})


@middleware
async def params_middleware(request, handler):
    """Обработчик входящего запроса."""
    white_list_urls = set(os.environ["WHITE_LIST_URLS"].split(","))
    path_components = set(request.path.split("/"))

    if request.path in white_list_urls or "swagger" in path_components:
        return await handler(request)

    content_dict = await load_contents(request.content_type)(request)
    result = await handler(**content_dict)
    return result


async def parse_multipart(request):
    """Извлечение параметров из запроса.

    Args:
        request: запрос

    Returns:
        dict: Словарь с данными запроса
    """
    fields = await request.multipart()
    result_dict = {}
    async for field in fields:
        file_name = field.filename
        size = 0
        file_path = f"static/{file_name}"
        async with async_open(file_path, "wb+") as fd:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                size += len(chunk)
                await fd.write(chunk)
        result_dict[field.name] = file_path

    return result_dict


async def parse_json(request):
    """Извлечение параметров из запроса.

    Args:
        request: запрос

    Returns:
        dict: Словарь с данными запроса
    """
    return await request.json()


async def parse_octet_stream(request):
    """Извлечение параметров из запроса.

    Args:
        request: запрос

    Returns:
        dict: Словарь с данными запроса
    """

    if request.query:
        return {k: request.query[k] for k in request.query.keys()}

    return {key: request.match_info[key] for key in request.match_info.keys()}


def load_contents(type_of_contents):
    """Фабричная метод, который определяет, какую функцию вызвать в зависимости от контекста.

    Args:
        type_of_contents(str): Тип контента

    Returns:
        function: Функция извлечения данных из запроса.
    """
    types = {
        "multipart/form-data": parse_multipart,
        "application/json": parse_json,
        "application/octet-stream": parse_octet_stream,
    }
    return types[type_of_contents]
