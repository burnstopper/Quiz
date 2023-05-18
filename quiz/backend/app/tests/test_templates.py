import json

from fastapi import status
from httpx import AsyncClient

from app.core.config import settings

created_template_1 = {
    'name': 'Created Template 1',
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
    ]
}

created_template_2 = {
    'name': 'Created Template 2',
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
    ]
}

created_template_3 = {
    'name': 'Created Template 3',
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
    ]
}

updated_template_1 = {
    'name': 'Updated Template 1',
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
    ]
}

template_1: dict[str, int | list | str] = updated_template_1.copy()
template_1['quizzes'] = []

template_2: dict[str, int | list | str] = created_template_2.copy()
template_2['quizzes'] = [
    {
        'name': 'Updated Quiz 2',
        'description': 'Test updating Quiz 2',
        'template_id': 2,
        'invite_link': f'http://{settings.HOST}:{settings.PORT}/invite/quizzes/2/add',
        'id': 2
    },
    {
        'name': 'Created Quiz 3',
        'description': 'Test creating Quiz 3',
        'template_id': 2,
        'invite_link': f'http://{settings.HOST}:{settings.PORT}/invite/quizzes/3/add',
        'id': 3
    }
]

template_3: dict[str, int | list | str] = created_template_3.copy()
template_3['quizzes'] = [
    {
        'name': 'Updated Quiz 1',
        'description': 'Test updating Quiz 1',
        'template_id': 3,
        'invite_link': f'http://{settings.HOST}:{settings.PORT}/invite/quizzes/1/add',
        'id': 1
    }
]


async def test_create_template(async_client: AsyncClient):
    # test creating a new template
    response = await async_client.post(url='/api/templates/', json={
        'name': 'Created Template 1',
        'tests_ids': [1, 2, 3]
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == created_template_1

    response = await async_client.post(url='/api/templates/', json={
        'name': 'Created Template 2',
        'tests_ids': [1, 2]
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == created_template_2

    response = await async_client.post(url='/api/templates/', json={
        'name': 'Created Template 3',
        'tests_ids': [4, 1]
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == created_template_3

    # test creating a new template with the name that already exists
    response = await async_client.post(url='/api/templates/', json={
        'name': ' Created Template 1 ',
        'tests_ids': [1, 2, 4]
    })
    assert response.status_code == status.HTTP_409_CONFLICT
    assert json.loads(response.content)['detail'] == 'Template with this name has already been created'

    # test creating a new template with invalid test id
    response = await async_client.post(url='/api/templates/', json={
        'name': 'Created Template 4',
        'tests_ids': [1, 2, 6]
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Invalid test id'


async def test_update_template(async_client: AsyncClient):
    # test updating the template by id
    response = await async_client.put(url='/api/templates/1', json={
        'name': 'Updated Template 1',
        'tests_ids': [2, 1, 3]
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == updated_template_1

    # test updating the template that has quizzes
    response = await async_client.put(url='/api/templates/2', json={
        'name': 'Updated Template 2',
        'tests_ids': [4, 1]
    })
    assert response.status_code == status.HTTP_409_CONFLICT
    assert json.loads(response.content)['detail'] == 'This template already has quizzes'

    # test updating the quiz by invalid id
    response = await async_client.put(url='/api/templates/4', json={
        'name': 'Test updating by invalid id',
        'tests_ids': [1, 2, 3]
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Template with this id does not exist'

    # test updating the template with the name that already exists
    response = await async_client.put(url='/api/templates/1', json={
        'name': ' Created Template 2 ',
        'tests_ids': [1, 2]
    })
    assert response.status_code == status.HTTP_409_CONFLICT
    assert json.loads(response.content)['detail'] == 'Template with this name has already been created'

    # test updating the template with invalid test id
    response = await async_client.put(url='/api/templates/1', json={
        'name': 'Updated Template 1',
        'tests_ids': [1, 2, 6]
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Invalid test id'


async def test_get_template_by_id(async_client: AsyncClient):
    # test getting the template by id
    response = await async_client.get(url='/api/templates/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == template_1

    # test getting the template by invalid id
    response = await async_client.get(url='/api/templates/4')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Template with this id does not exist'


async def test_get_all_templates(async_client: AsyncClient):
    # test getting all template with corresponding quizzes
    response = await async_client.get(url='/api/templates/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [template_1, template_2, template_3]
