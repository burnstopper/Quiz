import json

from fastapi import status
from httpx import AsyncClient

from app.api.templates import get_test_names_by_id


async def test_create_template(async_client: AsyncClient):
    # test creating a new template without name
    response = await async_client.post(url='/api/templates/', json={
        'name': '',
    })

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # test creating a new template
    tests_ids: list[int] = [1, 2, 3]
    tests_names: list[str] = [get_test_names_by_id(test_id=test) for test in tests_ids]

    response = await async_client.post(url='/api/templates/', json={
        'name': 'Template 1',
        'tests_ids': tests_ids
    })

    assert response.status_code == status.HTTP_201_CREATED

    assert response.json() == {
        'name': 'Template 1',
        'tests_ids': tests_ids,
        'tests_names': tests_names,
        'quizzes': None,
        'id': 1
    }

    # test creating a new template with the name that already exists
    response = await async_client.post(url='/api/templates/', json={
        'name': 'Template 1 ',
        'tests_ids': [1, 2, 4]
    })

    assert response.status_code == status.HTTP_409_CONFLICT

    # test creating a new template
    tests_ids: list[int] = [1, 2]
    tests_names: list[str] = [get_test_names_by_id(test_id=test) for test in tests_ids]

    response = await async_client.post(url='/api/templates/', json={
        'name': 'Template 2',
        'tests_ids': tests_ids,
    })

    assert response.status_code == status.HTTP_201_CREATED

    assert response.json() == {
        'name': 'Template 2',
        'tests_ids': tests_ids,
        'tests_names': tests_names,
        'quizzes': None,
        'id': 2
    }


async def test_update_template(async_client: AsyncClient):
    # test updating the template by id
    tests_ids: list[int] = [1, 2, 3]
    tests_names: list[str] = [get_test_names_by_id(test_id=test) for test in tests_ids]

    response = await async_client.put(url='/api/templates/1', json={
        'name': 'Updated Template 1',
        'tests_ids': tests_ids
    })

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        'name': 'Updated Template 1',
        'tests_ids': tests_ids,
        'tests_names': tests_names,
        'quizzes': None,
        'id': 1
    }

    # test updating the quiz by invalid id
    response = await async_client.put(url='/api/templates/3', json={
        'name': 'Updated Template 1',
        'tests_ids': [1, 2, 3]
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert json.loads(response.content)['detail'] == 'Template with this id has does not exist'

    # test updating the template with the name that already exists
    response = await async_client.put(url='/api/templates/2', json={
        'name': ' Updated Template 1 ',
        'tests_ids': [1, 2]
    })

    assert response.status_code == status.HTTP_409_CONFLICT

    assert json.loads(response.content)['detail'] == 'Template with this name has already been created'


async def test_get_all_templates(async_client: AsyncClient):
    # test getting all template with corresponding quizzes

    # create a new quiz
    response = await async_client.post(url='/api/quizzes/', json={
        'name': 'Quiz 3',
        'description': 'Create Quiz 3',
        'template_id': 2
    })

    assert response.status_code == status.HTTP_201_CREATED

    assert response.json() == {
        'name': 'Quiz 3',
        'description': 'Create Quiz 3',
        'template_id': 2,
        'id': 3
    }

    updated_template_first_tests_ids: list[int] = [1, 2, 3]
    updated_template_first_tests_names: list[str] = [get_test_names_by_id(test_id=test) for test in
                                                     updated_template_first_tests_ids]

    template_second_tests_ids: list[int] = [1, 2]
    template_second_tests_names: list[str] = [get_test_names_by_id(test_id=test) for test in template_second_tests_ids]

    response = await async_client.get(url='/api/templates/')

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == [
        {
            'name': 'Updated Template 1',
            'tests_ids': updated_template_first_tests_ids,
            'tests_names': updated_template_first_tests_names,
            'quizzes': [
                {
                    'name': 'Updated Quiz 1',
                    'description': 'Update Quiz 1',
                    'template_id': 1,
                    'id': 1
                }
            ],
            'id': 1
        },

        {
            'name': 'Template 2',
            'tests_ids': template_second_tests_ids,
            'tests_names': template_second_tests_names,
            'quizzes': [
                {
                    'name': 'Quiz 2',
                    'description': 'Create Quiz 2',
                    'template_id': 2,
                    'id': 2
                },

                {
                    'name': 'Quiz 3',
                    'description': 'Create Quiz 3',
                    'template_id': 2,
                    'id': 3
                }
            ],
            'id': 2
        }
    ]


async def test_get_template_by_id(async_client: AsyncClient):
    # test getting the template by id
    updated_template_first_tests_ids: list[int] = [1, 2, 3]
    updated_template_first_tests_names: list[str] = [get_test_names_by_id(test_id=test) for test in
                                                     updated_template_first_tests_ids]

    response = await async_client.get('/api/templates/1')

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        'name': 'Updated Template 1',
        'tests_ids': updated_template_first_tests_ids,
        'tests_names': updated_template_first_tests_names,
        'quizzes': [
            {
                'name': 'Updated Quiz 1',
                'description': 'Update Quiz 1',
                'template_id': 1,
                'id': 1
            }
        ],
        'id': 1
    }

    # test getting the template by invalid id
    response = await async_client.get('/api/templates/3')

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert json.loads(response.content)['detail'] == 'Template with this id has does not exist'
