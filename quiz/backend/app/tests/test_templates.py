import json

from fastapi import status
from httpx import AsyncClient

from app.core.config import settings


async def test_create_template(async_client: AsyncClient):
    # test creating a new template
    tests_ids = [1, 2, 3]
    tests_names = [settings.BURNOUT_SERVICE_NAME, settings.FATIGUE_SERVICE_NAME, settings.COPING_SERVICE_NAME]
    tests_urls = [settings.BURNOUT_SERVICE_URL, settings.FATIGUE_SERVICE_URL, settings.COPING_SERVICE_URL]

    response = await async_client.post(url='/api/templates/', json={
        'name': 'Created Template 1',
        'tests_ids': tests_ids
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'name': 'Created Template 1',
        'tests_ids': tests_ids,
        'tests_names': tests_names,
        'tests_urls': tests_urls,
        'quizzes': None,
        'id': 1
    }

    # test creating a new template with the name that already exists
    response = await async_client.post(url='/api/templates/', json={
        'name': ' Created Template 1 ',
        'tests_ids': [1, 2, 4]
    })
    assert response.status_code == status.HTTP_409_CONFLICT

    # test creating a new template
    tests_ids: list[int] = [1, 2]
    tests_names = [settings.BURNOUT_SERVICE_NAME, settings.FATIGUE_SERVICE_NAME]
    tests_urls = [settings.BURNOUT_SERVICE_URL, settings.FATIGUE_SERVICE_URL]

    response = await async_client.post(url='/api/templates/', json={
        'name': 'Created Template 2',
        'tests_ids': tests_ids,
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'name': 'Created Template 2',
        'tests_ids': tests_ids,
        'tests_names': tests_names,
        'tests_urls': tests_urls,
        'quizzes': None,
        'id': 2
    }


async def test_update_template(async_client: AsyncClient):
    # test updating the template by id
    updated_first_template_tests_ids = [2, 1, 3]
    updated_first_template_tests_names = [settings.FATIGUE_SERVICE_NAME, settings.BURNOUT_SERVICE_NAME,
                                          settings.COPING_SERVICE_NAME]
    updated_first_template_tests_urls = [settings.FATIGUE_SERVICE_URL, settings.BURNOUT_SERVICE_URL,
                                         settings.COPING_SERVICE_URL]

    response = await async_client.put(url='/api/templates/1', json={
        'name': 'Updated Template 1',
        'tests_ids': updated_first_template_tests_ids
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'name': 'Updated Template 1',
        'tests_ids': updated_first_template_tests_ids,
        'tests_names': updated_first_template_tests_names,
        'tests_urls': updated_first_template_tests_urls,
        'quizzes': None,
        'id': 1
    }

    updated_second_template_tests_ids = [4, 1]
    updated_second_template_tests_names = [settings.SPB_SERVICE_NAME, settings.BURNOUT_SERVICE_NAME]
    updated_second_template_tests_urls = [settings.SPB_SERVICE_URL, settings.BURNOUT_SERVICE_URL]

    response = await async_client.put(url='/api/templates/2', json={
        'name': 'Updated Template 2',
        'tests_ids': updated_second_template_tests_ids
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'name': 'Updated Template 2',
        'tests_ids': updated_second_template_tests_ids,
        'tests_names': updated_second_template_tests_names,
        'tests_urls': updated_second_template_tests_urls,
        'quizzes': None,
        'id': 2
    }

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
    updated_first_template_tests_ids = [2, 1, 3]
    updated_first_template_tests_names = [settings.FATIGUE_SERVICE_NAME, settings.BURNOUT_SERVICE_NAME,
                                          settings.COPING_SERVICE_NAME]
    updated_first_template_tests_urls = [settings.FATIGUE_SERVICE_URL, settings.BURNOUT_SERVICE_URL,
                                         settings.COPING_SERVICE_URL]

    response = await async_client.get('/api/templates/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'name': 'Updated Template 1',
        'tests_ids': updated_first_template_tests_ids,
        'tests_names': updated_first_template_tests_names,
        'tests_urls': updated_first_template_tests_urls,
        'quizzes': [
            {
                'name': 'Updated Quiz 1',
                'description': 'Test updating Quiz 1',
                'template_id': 1,
                'id': 1
            }
        ],
        'id': 1}

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

    updated_first_template_tests_ids = [2, 1, 3]
    updated_first_template_tests_names = [settings.FATIGUE_SERVICE_NAME, settings.BURNOUT_SERVICE_NAME,
                                          settings.COPING_SERVICE_NAME]
    updated_first_template_tests_urls = [settings.FATIGUE_SERVICE_URL, settings.BURNOUT_SERVICE_URL,
                                         settings.COPING_SERVICE_URL]

    updated_second_template_tests_ids = [4, 1]
    updated_second_template_tests_names = [settings.SPB_SERVICE_NAME, settings.BURNOUT_SERVICE_NAME]
    updated_second_template_tests_urls = [settings.SPB_SERVICE_URL, settings.BURNOUT_SERVICE_URL]

    response = await async_client.get(url='/api/templates/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'name': 'Updated Template 1',
            'tests_ids': updated_first_template_tests_ids,
            'tests_names': updated_first_template_tests_names,
            'tests_urls': updated_first_template_tests_urls,
            'quizzes': [
                {
                    'name': 'Updated Quiz 1',
                    'description': 'Test updating Quiz 1',
                    'template_id': 1,
                    'id': 1
                }
            ],
            'id': 1
        },

        {
            'name': 'Updated Template 2',
            'tests_ids': updated_second_template_tests_ids,
            'tests_names': updated_second_template_tests_names,
            'tests_urls': updated_second_template_tests_urls,
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
            ],
            'id': 2
        }
    ]
