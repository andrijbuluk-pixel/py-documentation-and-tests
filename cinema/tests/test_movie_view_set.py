from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from cinema.models import Movie, Genre, Actor
from cinema.serializers import MovieListSerializer, MovieDetailSerializer


class MovieViewSet(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test54431@test.com",
            password="test",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

        self.save_genres = Genre.objects.create(name="Fantasy")
        self.save_actors = Actor.objects.create(first_name="Test", last_name="User")

    def test_item_list(self) -> None:
        url = reverse("cinema:movie-list")
        res = self.client.get(url)

        items = Movie.objects.all()
        serializer = MovieListSerializer(items, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_item_detail(self) -> None:
        item = Movie.objects.create(
            title="test",
            description="test12211221",
            duration=120,
        )

        item.genres.set([self.save_genres])
        item.actors.set([self.save_actors])

        url = reverse("cinema:movie-detail", args=[item.id])
        res = self.client.get(url)

        serializer = MovieDetailSerializer(item)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_item_create(self) -> None:
        payload = {
            "title": "Test_title",
            "description": "Test_description",
            "duration": 90,
            "genres": [self.save_genres.id],
            "actors": [self.save_actors.id],
        }

        url = reverse("cinema:movie-list")
        res = self.client.post(url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 1)
