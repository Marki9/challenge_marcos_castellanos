from starlette.middleware.base import BaseHTTPMiddleware
import time

class ResponseTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        print(f"Request took {duration:.4f} seconds")
        return response