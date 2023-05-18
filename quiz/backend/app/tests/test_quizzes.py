import json

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import delete

from app.core.config import settings
from app.models.template import Template
from tests.conftest import async_session_maker

created_quiz_1 = {
    'name': 'Created Quiz 1',
    'description': 'Test creating Quiz 1',
    'template_id': 1,
    'invite_link': f'http://{settings.HOST}:{settings.PORT}/invite/quizzes/1/add',
    'id': 1
}

created_quiz_2 = {
    'name': 'Created Quiz 2',
    'description': 'Test creating Quiz 2',
    'template_id': 2,
    'invite_link': f'http://{settings.HOST}:{settings.PORT}/invite/quizzes/2/add',
    'id': 2
}

created_quiz_3 = {
    'name': 'Created Quiz 3',
    'description': 'Test creating Quiz 3',
    'template_id': 2,
    'invite_link': f'http://{settings.HOST}:{settings.PORT}/invite/quizzes/3/add',
    'id': 3
}

updated_quiz_1 = {
    'name': 'Updated Quiz 1',
    'description': 'Test updating Quiz 1',
    'template_id': 3,
    'invite_link': f'http://{settings.HOST}:{settings.PORT}/invite/quizzes/1/add',
    'id': 1
}

updated_quiz_2 = {
    'name': 'Updated Quiz 2',
    'description': 'Test updating Quiz 2',
    'template_id': 2,
    'invite_link': f'http://{settings.HOST}:{settings.PORT}/invite/quizzes/2/add',
    'id': 2
}

quiz_1 = updated_quiz_1
quiz_2 = updated_quiz_2
quiz_3 = created_quiz_3


@pytest.fixture(scope='module')
async def create_environment():
    async with async_session_maker() as session:
        template_1 = Template(name='Template 1')
        template_2 = Template(name='Template 2')
        template_3 = Template(name='Template 3')

        session.add_all([template_1, template_2, template_3])
        await session.commit()
    yield
    async with async_session_maker() as session:
        await session.execute(delete(Template))
        await session.commit()


async def test_create_quiz(async_client: AsyncClient, create_environment):
    # test creating a new quiz
    response = await async_client.post(url='/api/quizzes/', json={
        'name': 'Created Quiz 1',
        'description': 'Test creating Quiz 1',
        'template_id': 1
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == created_quiz_1

    response = await async_client.post(url='/api/quizzes/', json={
        'name': 'Created Quiz 2',
        'description': 'Test creating Quiz 2',
        'template_id': 2
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == created_quiz_2

    response = await async_client.post(url='/api/quizzes/', json={
        'name': 'Created Quiz 3',
        'description': 'Test creating Quiz 3',
        'template_id': 2,
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == quiz_3

    # test creating a new quiz with the name that already exists
    response = await async_client.post(url='/api/quizzes/', json={
        'name': ' Created Quiz 1 ',
        'description': 'Test conflicts with Quiz 1',
        'template_id': 1
    })
    assert response.status_code == status.HTTP_409_CONFLICT
    assert json.loads(response.content)['detail'] == 'Quiz with this name already has been created'


async def test_update_quiz(async_client: AsyncClient):
    # test updating the quiz by id
    response = await async_client.put(url='/api/quizzes/1', json={
        'name': 'Updated Quiz 1',
        'description': 'Test updating Quiz 1',
        'template_id': 3
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == updated_quiz_1

    response = await async_client.put(url='/api/quizzes/2', json={
        'name': 'Updated Quiz 2',
        'description': 'Test updating Quiz 2',
        'template_id': 2
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == updated_quiz_2

    # test updating the quiz by invalid id
    response = await async_client.put(url='/api/quizzes/4', json={
        'name': 'Quiz updated by invalid id',
        'description': 'Testing updating by invalid id',
        'template_id': 2
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Quiz with this id does not exist'

    # test updating the quiz with the name that already exists
    response = await async_client.put(url='/api/quizzes/1', json={
        'name': ' Updated Quiz 2 ',
        'description': 'Test updating Quiz 2',
        'template_id': 2
    })
    assert response.status_code == status.HTTP_409_CONFLICT
    assert json.loads(response.content)['detail'] == 'Quiz with this name already has been created'


async def test_add_respondent_to_quiz(async_client: AsyncClient):
    # test adding a respondent to quiz
    respondent_id: int = 1
    response = await async_client.post(url='/invite/quizzes/1/add', params={'respondent_id': respondent_id})
    assert response.status_code == status.HTTP_200_OK

    respondent_id: int = 1
    response = await async_client.post(url='/invite/quizzes/2/add', params={'respondent_id': respondent_id})
    assert response.status_code == status.HTTP_200_OK

    respondent_id: int = 2
    response = await async_client.post(url='/invite/quizzes/1/add', params={'respondent_id': respondent_id})
    assert response.status_code == status.HTTP_200_OK

    # test adding the respondent who has been added
    response = await async_client.post(url='/invite/quizzes/1/add', params={'respondent_id': respondent_id})
    assert response.status_code == status.HTTP_409_CONFLICT
    assert json.loads(response.content)['detail'] == 'Respondent has already added to quiz'

    # test adding a respondent to quiz with invalid quiz_id
    response = await async_client.post(url='/invite/quizzes/4/add', params={'respondent_id': respondent_id})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Invalid invite link: quiz with this id does not exist'


async def test_has_access_to_quiz(async_client: AsyncClient):
    # test checking has the respondent access to quiz
    respondent_id: int = 1
    response = await async_client.get(url='/api/quizzes/1/check_access', params={'respondent_id': respondent_id})
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content)['has_access']

    response = await async_client.get(url='/api/quizzes/1/check_access', params={'respondent_id': 123})
    assert response.status_code == status.HTTP_200_OK
    assert not json.loads(response.content)['has_access']

    # test checking has the respondent access to quiz with invalid id
    response = await async_client.get(url='/api/quizzes/4/check_access', params={'respondent_id': 123})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Quiz with this id does not exist'


async def test_get_quiz_respondents(async_client: AsyncClient):
    # test getting quiz respondents
    response = await async_client.get(url='/api/quizzes/1/respondents')
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content)['respondents'] == [1, 2]

    # test getting quiz respondents by invalid id
    response = await async_client.get(url='/api/quizzes/4/respondents')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Quiz with this id does not exist'


async def test_get_quiz_by_id(async_client: AsyncClient):
    # test getting the quiz by id
    response = await async_client.get(url='/api/quizzes/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == quiz_1

    # test getting the quiz by invalid id
    response = await async_client.get(url='/api/quizzes/4')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Quiz with this id does not exist'


async def test_get_quizzes(async_client: AsyncClient):
    # test getting all quizzes
    response = await async_client.get(url='/api/quizzes/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [quiz_1, quiz_2, quiz_3]

    # test getting respondent quizzes
    respondent_id: int = 1
    response = await async_client.get(url='/api/quizzes/', params={'respondent_id': 1})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [quiz_1, quiz_2]
