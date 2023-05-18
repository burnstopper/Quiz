import json

from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select

from app.core.config import settings
from app.models.quiz import Quiz
from tests.conftest import async_session_maker
from tests.test_quizzes import quiz_1, quiz_2, quiz_3

created_template_1 = {
    'name': 'Created FullTemplate 1',
    'id': 1,
    'tests': [
        {
            'id': 1,
            'name': settings.BURNOUT_SERVICE_NAME,
            'url': settings.BURNOUT_SERVICE_URL
        },
        {
            'id': 2,
            'name': settings.FATIGUE_SERVICE_NAME,
            'url': settings.FATIGUE_SERVICE_URL
        },
        {
            'id': 3,
            'name': settings.COPING_SERVICE_NAME,
            'url': settings.COPING_SERVICE_URL
        }
    ],
    'quizzes': None
}

created_template_2 = {
    'name': 'Created FullTemplate 2',
    'id': 2,
    'tests': [
        {
            'id': 1,
            'name': settings.BURNOUT_SERVICE_NAME,
            'url': settings.BURNOUT_SERVICE_URL
        },
        {
            'id': 2,
            'name': settings.FATIGUE_SERVICE_NAME,
            'url': settings.FATIGUE_SERVICE_URL
        }
    ],
    'quizzes': None
}

created_template_3 = {
    'name': 'Created FullTemplate 3',
    'id': 3,
    'tests': [
        {
            'id': 4,
            'name': settings.SPB_SERVICE_NAME,
            'url': settings.SPB_SERVICE_URL
        },
        {
            'id': 1,
            'name': settings.BURNOUT_SERVICE_NAME,
            'url': settings.BURNOUT_SERVICE_URL
        }
    ],
    'quizzes': None
}

updated_template_1 = {
    'name': 'Updated FullTemplate 1',
    'id': 1,
    'tests': [
        {
            'id': 2,
            'name': settings.FATIGUE_SERVICE_NAME,
            'url': settings.FATIGUE_SERVICE_URL
        },
        {
            'id': 1,
            'name': settings.BURNOUT_SERVICE_NAME,
            'url': settings.BURNOUT_SERVICE_URL
        },
        {
            'id': 3,
            'name': settings.COPING_SERVICE_NAME,
            'url': settings.COPING_SERVICE_URL
        }
    ],
    'quizzes': None
}

template_1 = {
    'name': 'Updated FullTemplate 1',
    'id': 1,
    'tests': [
        {
            'id': 2,
            'name': settings.FATIGUE_SERVICE_NAME,
            'url': settings.FATIGUE_SERVICE_URL
        },
        {
            'id': 1,
            'name': settings.BURNOUT_SERVICE_NAME,
            'url': settings.BURNOUT_SERVICE_URL
        },
        {
            'id': 3,
            'name': settings.COPING_SERVICE_NAME,
            'url': settings.COPING_SERVICE_URL
        }
    ],
    'quizzes': []
}

template_2 = created_template_2
template_3 = created_template_3
template_3['quizzes'] = [quiz_3]


async def test_create_template(async_client: AsyncClient):
    # test creating a new template
    tests_ids = [1, 2, 3]
    response = await async_client.post(url='/api/templates/', json={
        'name': 'Created FullTemplate 1',
        'tests_ids': tests_ids
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == created_template_1

    tests_ids: list[int] = [1, 2]
    response = await async_client.post(url='/api/templates/', json={
        'name': 'Created FullTemplate 2',
        'tests_ids': tests_ids,
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == created_template_2

    # test creating a new template with the name that already exists
    response = await async_client.post(url='/api/templates/', json={
        'name': ' Created FullTemplate 1 ',
        'tests_ids': [1, 2, 4]
    })
    assert response.status_code == status.HTTP_409_CONFLICT

    tests_ids = [4, 1]
    response = await async_client.post(url='/api/templates/', json={
        'name': 'Created FullTemplate 3',
        'tests_ids': tests_ids
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == created_template_3


async def test_update_template(async_client: AsyncClient):
    # test updating the template by id
    updated_first_template_tests_ids = [2, 1, 3]
    response = await async_client.put(url='/api/templates/1', json={
        'name': 'Updated FullTemplate 1',
        'tests_ids': updated_first_template_tests_ids
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == updated_template_1

    # tes updating the template that has quizzes
    updated_second_template_tests_ids = [4, 1]
    response = await async_client.put(url='/api/templates/2', json={
        'name': 'Updated FullTemplate 2',
        'tests_ids': updated_second_template_tests_ids
    })
    assert response.status_code != status.HTTP_409_CONFLICT
    assert json.loads(response.content)['detail'] == 'This template already has quizzes'

    # test updating the quiz by invalid id
    response = await async_client.put(url='/api/templates/4', json={
        'name': 'Test updating by invalid id',
        'tests_ids': [1, 2, 3]
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'FullTemplate with this id does not exist'

    # test updating the template with the name that already exists
    response = await async_client.put(url='/api/templates/1', json={
        'name': ' Updated FullTemplate 2 ',
        'tests_ids': [1, 2]
    })
    assert response.status_code == status.HTTP_409_CONFLICT
    assert json.loads(response.content)['detail'] == 'FullTemplate with this name has already been created'


async def test_get_template_by_id(async_client: AsyncClient):
    # test getting the template by id
    response = await async_client.get(url='/api/templates/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == template_1

    # test getting the template by invalid id
    response = await async_client.get(url='/api/templates/4')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'FullTemplate with this id does not exist'


async def test_get_all_templates(async_client: AsyncClient):
    # test getting all template with corresponding quizzes
    response = await async_client.get(url='/api/templates/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [template_1, template_2]
