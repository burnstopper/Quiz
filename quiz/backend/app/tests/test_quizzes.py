import json

from fastapi import status
from httpx import AsyncClient


async def test_create_quiz(async_client: AsyncClient):
    # test creating a new quiz
    response = await async_client.post(url='/api/quizzes/', json={
        'name': 'Created Quiz 1',
        'description': 'Test creating Quiz 1',
        'template_id': 1
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'name': 'Created Quiz 1',
        'description': 'Test creating Quiz 1',
        'template_id': 1,
        'id': 1
    }

    # test creating a new quiz with the name that already exists
    response = await async_client.post(url='/api/quizzes/', json={
        'name': ' Created Quiz 1 ',
        'description': 'Test conflicts with Quiz 1',
        'template_id': 1
    })
    assert response.status_code == status.HTTP_409_CONFLICT

    # test creating a new quiz
    response = await async_client.post(url='/api/quizzes/', json={
        'name': 'Created Quiz 2',
        'description': 'Test creating Quiz 2',
        'template_id': 2
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'name': 'Created Quiz 2',
        'description': 'Test creating Quiz 2',
        'template_id': 2,
        'id': 2
    }


async def test_update_quiz(async_client: AsyncClient):
    # test updating the quiz by id
    response = await async_client.put(url='/api/quizzes/1', json={
        'name': 'Updated Quiz 1',
        'description': 'Test updating Quiz 1',
        'template_id': 1
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'name': 'Updated Quiz 1',
        'description': 'Test updating Quiz 1',
        'template_id': 1,
        'id': 1
    }

    response = await async_client.put(url='/api/quizzes/2', json={
        'name': 'Updated Quiz 2',
        'description': 'Test updating Quiz 2',
        'template_id': 2
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'name': 'Updated Quiz 2',
        'description': 'Test updating Quiz 2',
        'template_id': 2,
        'id': 2
    }

    # test updating the quiz by invalid id
    response = await async_client.put(url='/api/quizzes/3', json={
        'name': 'Quiz updated by invalid id',
        'description': 'Testing updating by invalid id',
        'template_id': 2
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Quiz with this id does not exist'

    # test updating the quiz with the name that already exists
    response = await async_client.put(url='/api/quizzes/1', json={
        'name': 'Updated Quiz 2 ',
        'description': 'Test updating Quiz 2',
        'template_id': 2
    })
    assert response.status_code == status.HTTP_409_CONFLICT
    assert json.loads(response.content)['detail'] == 'Quiz with this name has already been created'


async def test_get_quiz_by_id(async_client: AsyncClient):
    # test getting the quiz by id
    response = await async_client.get('/api/quizzes/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'name': 'Updated Quiz 1',
        'description': 'Test updating Quiz 1',
        'template_id': 1,
        'id': 1
    }

    # test getting the quiz by invalid id
    response = await async_client.get('/api/quizzes/3')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Quiz with this id does not exist'


async def test_get_quizzes(async_client: AsyncClient):
    # test getting all quizzes
    response = await async_client.get('/api/quizzes/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'name': 'Updated Quiz 1',
            'description': 'Test updating Quiz 1',
            'template_id': 1,
            'id': 1
        },
        {
            'name': 'Updated Quiz 2',
            'description': 'Test updating Quiz 2',
            'template_id': 2,
            'id': 2
        }
    ]
