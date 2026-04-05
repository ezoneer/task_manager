import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time
        # 4. Добавляем заголовок (для браузера)
        response.headers["X-Process-Time"] = str(process_time)

        # 5. Выводим в консоль (для тебя)
        print(f"DEBUG: Путь {request.url.path} занял {process_time:.4f} сек")

        return response