import json

import httpx
from fastapi import APIRouter, status, HTTPException

from app.core.config import settings

router = APIRouter()


@router.get('/{respondent_token}', status_code=status.HTTP_200_OK)
async def get_respondent_id_by_token(respondent_token: str) -> dict[str, int]:
    """
    Get the respondent id by token
    """

    # sets retries amount to 10 and if after this User microservice does not respond - raise normal exception (5xx)
    transport = httpx.AsyncHTTPTransport(retries=10)
    timeout = httpx.Timeout(1.0)
    async with httpx.AsyncClient(transport=transport, timeout=timeout) as client:
        response = (await client.get(f'http://{settings.HOST}:{settings.TOKEN_SERVICE_PORT}'
                                     f'/api/user/{respondent_token}',
                                     headers={'Authorization': f'Bearer {settings.BEARER_TOKEN}'})
                    )

        if response.status_code == status.HTTP_403_FORBIDDEN:
            raise HTTPException(status_code=response.status_code, detail=json.loads(response.content)['detail'])

        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(status_code=response.status_code, detail=json.loads(response.content)['detail'])

        respondent_id = int(response.text)

    return {'respondent_id': respondent_id}


@router.post('/create_respondent', status_code=status.HTTP_201_CREATED)
async def create_new_respondent() -> dict[str, str]:
    """
    Create a new respondent
    """

    # sets retries amount to 10 and if after this User microservice does not respond - raise normal exception (5xx)
    transport = httpx.AsyncHTTPTransport(retries=10)
    timeout = httpx.Timeout(1.0)
    async with httpx.AsyncClient(transport=transport, timeout=timeout) as client:
        respondent_token = (await client.post(f'http://{settings.HOST}:{settings.TOKEN_SERVICE_PORT}'
                                              f'/api/user/new_respondent',
                                              headers={'Authorization': f'Bearer {settings.BEARER_TOKEN}'})
                            ).text

    return {'respondent_token': respondent_token}
