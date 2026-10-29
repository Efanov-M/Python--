import pytest

from django.urls import reverse
from rest_framework import status

from students.models import Course


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    course = course_factory(name="Python")

    url = reverse("courses-detail", args=[course.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == course.id
    assert response.data["name"] == course.name


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    course_1 = course_factory(name="Python")
    course_2 = course_factory(name="Django")

    url = reverse("courses-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    course_ids = [course["id"] for course in response.data]

    assert course_1.id in course_ids
    assert course_2.id in course_ids


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    course_1 = course_factory(name="Python")
    course_factory(name="Django")

    url = reverse("courses-list")
    response = api_client.get(url, data={"id": course_1.id})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == course_1.id
    assert response.data[0]["name"] == course_1.name


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    course_1 = course_factory(name="Python")
    course_factory(name="Django")

    url = reverse("courses-list")
    response = api_client.get(url, data={"name": course_1.name})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == course_1.id
    assert response.data[0]["name"] == course_1.name


@pytest.mark.django_db
def test_create_course(api_client):
    url = reverse("courses-list")

    data = {
        "name": "Python",
        "students": [],
    }

    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == data["name"]
    assert Course.objects.filter(name="Python").exists()


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course = course_factory(name="Python")

    url = reverse("courses-detail", args=[course.id])

    data = {
        "name": "Django",
        "students": [],
    }

    response = api_client.put(url, data=data, format="json")

    assert response.status_code == status.HTTP_200_OK

    course.refresh_from_db()

    assert course.name == "Django"
    assert response.data["name"] == "Django"


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory(name="Python")

    url = reverse("courses-detail", args=[course.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Course.objects.filter(id=course.id).exists()
