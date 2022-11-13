from fastapi import BackgroundTasks, FastAPI
from typing import Union
import httpx
import time
from settings import SERVERS_ADDRESSES


app = FastAPI()

servers = SERVERS_ADDRESSES


@app.get("/{path:path}")
async def balancer(background_health_check: BackgroundTasks, servers: list, path: Union[str, None] = None):
    """
    Реализован алгоритм балансировки Round-robin

    """
    try:
        host_name = servers.pop(0)
    except IndexError:
        return 'host not found'
    host_name = check_status_server(host_name, background_health_check)
    async with httpx.AsyncClient() as client:
        response = await client.get(f'http://{host_name}/{path}')
        servers.append(host_name)
    return response.content


def check_status_server(host_name, background_health_check):
    """
    Проверка состояния сервера
    Если не отвечает - отправляем в health_check

    """
    try:
        httpx.get(f'http://{host_name}/health/')
        return host_name
    except httpx.ConnectError:
        background_health_check.add_task(health_check, host_name)
        try:
            host_name = servers.pop(0)
            return check_status_server(host_name, background_health_check)
        except IndexError:
            return 'host not found'


def health_check(host_name):
    """
    Фоновая проверка состояния сервера, каждые 5 секунд
    Получая ответ от сервера добавляем его в список servers

    """
    while True:
        time.sleep(5)
        try:
            httpx.get(f'http://{host_name}/health/')
            servers.append(host_name)
            break
        except httpx.ConnectError:
            continue
