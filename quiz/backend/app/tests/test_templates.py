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
    ],
    'quizzes': None
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
    ],
    'quizzes': None
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
    ],
    'quizzes': None
}

updated_template_2 = {
    'name': 'Updated Template 2',
    'id': 2,
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

template_1 = {
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
    ],
    'quizzes': [
        {
            'name': 'Updated Quiz 1',
            'description': 'Test updating Quiz 1',
            'template_id': 1,
            'id': 1
        }
    ]
}

template_2 = {
    'name': 'Updated Template 2',
    'id': 2,
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
    'quizzes': [
        {
            'name': 'Updated Quiz 2',
            'description': 'Test updating Quiz 2',
            'template_id': 2,
            'id': 2
        },

        {
            'name': 'Created Quiz 3',
            'description': 'Test creating Quiz 3',
            'template_id': 2,
            'id': 3
        }
    ]
}


async def test_create_template(async_client: AsyncClient):
    # test creating a new template
    tests_ids = [1, 2, 3]
    response = await async_client.post(url='/api/templates/', json={
        'name': 'Created Template 1',
        'tests_ids': tests_ids
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == created_template_1

    tests_ids: list[int] = [1, 2]
    response = await async_client.post(url='/api/templates/', json={
        'name': 'Created Template 2',
        'tests_ids': tests_ids,
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == created_template_2

    # test creating a new template with the name that already exists
    response = await async_client.post(url='/api/templates/', json={
        'name': ' Created Template 1 ',
        'tests_ids': [1, 2, 4]
    })
    assert response.status_code == status.HTTP_409_CONFLICT


async def test_update_template(async_client: AsyncClient):
    # test updating the template by id
    updated_first_template_tests_ids = [2, 1, 3]
    response = await async_client.put(url='/api/templates/1', json={
        'name': 'Updated Template 1',
        'tests_ids': updated_first_template_tests_ids
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == updated_template_1

    updated_second_template_tests_ids = [4, 1]
    response = await async_client.put(url='/api/templates/2', json={
        'name': 'Updated Template 2',
        'tests_ids': updated_second_template_tests_ids
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == updated_template_2

    # test updating the quiz by invalid id
    response = await async_client.put(url='/api/templates/3', json={
        'name': 'Test updating by invalid id',
        'tests_ids': [1, 2, 3]
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Template with this id does not exist'

    # test updating the template with the name that already exists
    response = await async_client.put(url='/api/templates/1', json={
        'name': ' Updated Template 2 ',
        'tests_ids': [1, 2]
    })
    assert response.status_code == status.HTTP_409_CONFLICT
    assert json.loads(response.content)['detail'] == 'Template with this name has already been created'


async def test_get_template_by_id(async_client: AsyncClient):
    # test getting the template by id
    response = await async_client.get('/api/templates/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == template_1

    # test getting the template by invalid id
    response = await async_client.get('/api/templates/3')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Template with this id does not exist'


async def test_get_all_templates(async_client: AsyncClient):
    # test getting all template with corresponding quizzes

    # create a new quiz
    response = await async_client.post(url='/api/quizzes/', json={
        'name': 'Created Quiz 3',
        'description': 'Test creating Quiz 3',
        'template_id': 2,
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'name': 'Created Quiz 3',
        'description': 'Test creating Quiz 3',
        'template_id': 2,
        'id': 3
    }

    response = await async_client.get(url='/api/templates/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [template_1, template_2]
