from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import api_router
from app.core.config import settings

app = FastAPI()
app.include_router(api_router)

# at current no actual origins added
origins = [
    f'http://{settings.HOST}:8001',
    f'https://{settings.HOST}:8001',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8001, log_level='debug')
