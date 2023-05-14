import json

from fastapi import status
from httpx import AsyncClient

created_quiz_1 = {
    'name': 'Created Quiz 1',
    'description': 'Test creating Quiz 1',
    'template_id': 1,
    'invite_link': '/invite/quizzes/1/add',
    'id': 1
}

created_quiz_2 = {
    'name': 'Created Quiz 2',
    'description': 'Test creating Quiz 2',
    'template_id': 2,
    'invite_link': '/invite/quizzes/2/add',
    'id': 2
}

updated_quiz_1 = {
    'name': 'Updated Quiz 1',
    'description': 'Test updating Quiz 1',
    'template_id': 1,
    'invite_link': '/invite/quizzes/1/add',
    'id': 1
}

updated_quiz_2 = {
    'name': 'Updated Quiz 2',
    'description': 'Test updating Quiz 2',
    'template_id': 2,
    'invite_link': '/invite/quizzes/2/add',
    'id': 2
}

quiz_1 = updated_quiz_1
quiz_2 = updated_quiz_2
quiz_3 = {
    'name': 'Created Quiz 3',
    'description': 'Test creating Quiz 3',
    'template_id': 2,
    'invite_link': '/invite/quizzes/3/add',
    'id': 3
}


async def test_create_quiz(async_client: AsyncClient):
    # test creating a new quiz
    response = await async_client.post(url='/api/quizzes/', json={
        'name': 'Created Quiz 1',
        'description': 'Test creating Quiz 1',
        'template_id': 1
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == created_quiz_1

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
    assert response.json() == created_quiz_2

    response = await async_client.post(url='/api/quizzes/', json={
        'name': 'Created Quiz 3',
        'description': 'Test creating Quiz 3',
        'template_id': 2,
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == quiz_3


async def test_update_quiz(async_client: AsyncClient):
    # test updating the quiz by id
    response = await async_client.put(url='/api/quizzes/1', json={
        'name': 'Updated Quiz 1',
        'description': 'Test updating Quiz 1',
        'template_id': 1
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
        'name': 'Updated Quiz 2 ',
        'description': 'Test updating Quiz 2',
        'template_id': 2
    })
    assert response.status_code == status.HTTP_409_CONFLICT
    assert json.loads(response.content)['detail'] == 'Quiz with this name has already been created'


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


async def test_add_respondent_to_quiz(async_client: AsyncClient):
    # test adding a respondent to quiz
    respondent_token: str = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..WjB9WSQCkIeBBHIpwJqjzg' \
                            '.Z9xL_sDFXah58hUpOoWbBkcYglypM-M1HGPMC0CQEueZOLMUfvNqki5SBzTd_nq9TGy' \
                            '-sM8eBAAOyboPXjhAFdqNI8kVLl-UWuv4WLmiC_Uao1zlPElcStbJhk5dwIgunXxrdmJ44vDBRjs9TcxbOqiiLCv' \
                            '-YYsi708L__WmdzoVtYhdEbLzgSDIkSDMoM_SPDdKYDc1mQ.TMo_7yG9IhUOju9kS4LELg'

    response = await async_client.post(url='/invite/quizzes/1/add', params={'respondent_token': respondent_token})
    assert response.status_code == status.HTTP_200_OK

    # test adding the respondent who has been added
    response = await async_client.post(url='/invite/quizzes/1/add', params={'respondent_token': respondent_token})
    assert response.status_code == status.HTTP_409_CONFLICT
    assert json.loads(response.content)['detail'] == 'Respondent has already added to quiz'

    # test adding a respondent to quiz with invalid quiz_id
    response = await async_client.post(url='/invite/quizzes/4/add', params={'respondent_token': respondent_token})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content)['detail'] == 'Invalid invite link: quiz with this id does not exist'

    # test adding a respondent with invalid token
    response = await async_client.post(url='/invite/quizzes/2/add', params={'respondent_token': 'invalid token'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert json.loads(response.content)['detail'] == 'Invalid token'


async def test_has_access_to_quiz(async_client: AsyncClient):
    # test checking has a respondent access to quiz
    respondent_token: str = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..WjB9WSQCkIeBBHIpwJqjzg' \
                            '.Z9xL_sDFXah58hUpOoWbBkcYglypM-M1HGPMC0CQEueZOLMUfvNqki5SBzTd_nq9TGy' \
                            '-sM8eBAAOyboPXjhAFdqNI8kVLl-UWuv4WLmiC_Uao1zlPElcStbJhk5dwIgunXxrdmJ44vDBRjs9TcxbOqiiLCv' \
                            '-YYsi708L__WmdzoVtYhdEbLzgSDIkSDMoM_SPDdKYDc1mQ.TMo_7yG9IhUOju9kS4LELg'

    response = await async_client.get(url=f'/api/token/{respondent_token}/id')
    assert response.status_code == status.HTTP_200_OK

    respondent_id: int = json.loads(response.content)['respondent_id']
    response = await async_client.get(url='/api/quizzes/1/check_access', params={'respondent_id': respondent_id})
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content)['has_access']

    # test getting respondent quizzes
    response = await async_client.get(url='/api/quizzes/', params={'respondent_id': respondent_id})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [quiz_1]

    response = await async_client.get(url='/api/quizzes/1/check_access', params={'respondent_id': 123})
    assert response.status_code == status.HTTP_200_OK
    assert not json.loads(response.content)['has_access']
