import json

from fastapi import status
from httpx import AsyncClient


async def test_create_new_respondent_and_get_respondent_id(async_client: AsyncClient):
    # test creating a new respondent
    response = await async_client.post(url='/api/token/create_respondent')
    assert response.status_code == status.HTTP_201_CREATED

    respondent_token: str = json.loads(response.content)['respondent_token']

    # test getting the respondent id by invalid token
    response = await async_client.get(url='/api/token/blablabla/id')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert json.loads(response.content)['detail'] == 'Invalid token'

    # test getting the respondent id by valid token
    response = await async_client.get(url=f'/api/token/{respondent_token}/id')
    assert response.status_code == status.HTTP_200_OK
