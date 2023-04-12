from fastapi import status
from httpx import AsyncClient
import json


async def test_create_quiz(async_client: AsyncClient):
    # test creating a new quiz
    response = await async_client.post(url='/api/quizzes/', json={
        'name': 'Quiz 1',
        'description': 'Create Quiz 1',
        'template_id': 1
    })

    assert response.status_code == status.HTTP_201_CREATED

    assert response.json() == {
        'name': 'Quiz 1',
        'description': 'Create Quiz 1',
        'template_id': 1,
        'id': 1
    }

    # test creating a new quiz with the name that already exists
    response = await async_client.post(url='/api/quizzes/', json={
        'name': 'Quiz 1 ',
        'description': 'Create Quiz 1',
        'template_id': 1
    })

    assert response.status_code == status.HTTP_409_CONFLICT

    # test creating a new quiz
    response = await async_client.post(url='/api/quizzes/', json={
        'name': 'Quiz 2',
        'description': 'Create Quiz 2',
        'template_id': 2
    })

    assert response.status_code == status.HTTP_201_CREATED

    assert response.json() == {
        'name': 'Quiz 2',
        'description': 'Create Quiz 2',
        'template_id': 2,
        'id': 2
    }


async def test_update_quiz(async_client: AsyncClient):
    # test updating the quiz by id
    response = await async_client.put(url='/api/quizzes/1', json={
        'name': 'Updated Quiz 1',
        'description': 'Update Quiz 1',
        'template_id': 2
    })

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        'name': 'Updated Quiz 1',
        'description': 'Update Quiz 1',
        'template_id': 2,
        'id': 1
    }

    # test updating the quiz by invalid id
    response = await async_client.put(url='/api/quizzes/3', json={
        'name': 'Updated Quiz 1',
        'description': 'Update Quiz 1',
        'template_id': 2
    })

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert json.loads(response.content)['detail'] == 'Quiz with this id has does not exist'

    # test updating the quiz with the name that already exists
    response = await async_client.put(url='/api/quizzes/2', json={
        'name': 'Updated Quiz 1 ',
        'description': 'Update Quiz 2',
        'template_id': 3
    })

    assert response.status_code == status.HTTP_409_CONFLICT

    assert json.loads(response.content)['detail'] == 'Quiz with this name has already been created'


async def test_get_quizzes(async_client: AsyncClient):
    # test getting all quizzes
    response = await async_client.get('/api/quizzes/')

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == [
        {
            'name': 'Updated Quiz 1',
            'description': 'Update Quiz 1',
            'template_id': 2,
            'id': 1
        },
        {
            'name': 'Quiz 2',
            'description': 'Create Quiz 2',
            'template_id': 2,
            'id': 2
        }
    ]


async def test_get_quiz_by_id(async_client: AsyncClient):
    # test getting the quiz by id
    response = await async_client.get('/api/quizzes/1')

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        'name': 'Updated Quiz 1',
        'description': 'Update Quiz 1',
        'template_id': 2,
        'id': 1
    }

    # test getting the quiz by invalid id
    response = await async_client.get('/api/quizzes/3')

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert json.loads(response.content)['detail'] == 'Quiz with this id has does not exist'
