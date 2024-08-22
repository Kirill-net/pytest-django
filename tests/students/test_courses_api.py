import random

import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_first_courses(client, courses_factory):
    cours = courses_factory(_quantity=1)
    response = client.get('/courses/')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == cours[0].name


@pytest.mark.django_db
def test_get_list_courses(client, courses_factory):
    list_courses = courses_factory(_quantity=10)

    response = client.get('/courses/')
    data_list = response.json()

    assert response.status_code == 200
    for i, d in enumerate(data_list):
        assert d['name'] == list_courses[i].name


@pytest.mark.django_db
def test_filter_id_courses(client, courses_factory):
    list_courses = courses_factory(_quantity=10)
    r = random.randint(0,9)
    id_course = list_courses[r].id

    response = client.get(f'/courses/?id={id_course}')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == list_courses[r].name


@pytest.mark.django_db
def test_filter_name_courses(client, courses_factory):
    list_courses = courses_factory(_quantity=10)
    r = random.randint(0,9)
    name_course = list_courses[r].name

    response = client.get(f'/courses/?name={name_course}')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == list_courses[r].name


@pytest.mark.django_db
def test_create_course(client):
    count_before = Course.objects.count()
    data = {
        'name': 'python',
        'students': []
        }
    response = client.post('/courses/', data)

    assert response.status_code == 201
    assert Course.objects.count() == count_before + 1


@pytest.mark.django_db
def test_patch_course(client, courses_factory):
    list_courses = courses_factory(_quantity=10)
    r = random.randint(0,9)
    id_course = list_courses[r].id
    data = {
        'name': 'python',
        'students': []
    }

    response = client.patch(f'/courses/{id_course}/', data)
    result = Course.objects.filter(id=id_course).first()

    assert response.status_code == 200
    assert result.name == 'python'


@pytest.mark.django_db
def test_delete_course(client, courses_factory):
    list_courses = courses_factory(_quantity=10)
    r = random.randint(0, 9)
    id_course = list_courses[r].id
    count_before = Course.objects.count()

    response = client.delete(f'/courses/{id_course}/')

    assert response.status_code == 204
    assert Course.objects.count() == count_before - 1

