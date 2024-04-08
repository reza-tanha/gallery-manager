from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
User = get_user_model()


class MediaTest(TestCase):

    def create_user_db(self, email: str, password: str) -> User:
        return User.objects.create_user(
            email=email,
            password=password
        )

    def login_user(self, email: str, password: str) -> None:
        self.cli = APIClient()
        res = self.cli.post('/api/auth/jwt/login/', data={"email": email, "password": password})
        self.cli.credentials(HTTP_AUTHORIZATION=f'Bearer {res.json()["access"]}')

    def setUp(self) -> None:
        self.email = "reza@email.com"
        self.password = "rezareza123!@#"
        self.create_user_db(self.email, self.password)
        self.login_user(self.email, self.password)
        return super().setUp()

    def test_add_media(self) -> None:
        response = self.cli.post('/api/media/', 
            data={
                "name" : "image_name",
                "description": "this is test"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "image_name")

    def test_list_media(self) -> None:
        response = self.cli.get('/api/media/', format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_media(self) -> None:
        response = self.cli.post('/api/media/', 
            data={
                "name" : "image_name",
                "description": "this is test"
            }
        )
        self.assertEqual(response.status_code, 201)
        response = self.cli.get(f'/api/media/{response.json()["id"]}/', format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()['file'])

    def test_put_media(self) -> None:
        response = self.cli.post('/api/media/', 
            data={
                "name" : "image_name",
                "description": "this is test"
            }
        )
        self.assertEqual(response.status_code, 201)
        response = self.cli.put(
            f'/api/media/{response.json()["id"]}/',
            format="json",
            data={
                "name" : "new_name"
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "new_name")

    def test_delete_media(self) -> None:
        response = self.cli.post('/api/media/', 
            data={
                "name" : "image_name",
                "description": "this is test"
            }
        )
        self.assertEqual(response.status_code, 201)
        response = self.cli.delete(f'/api/media/{response.json()["id"]}/')
        self.assertEqual(response.status_code, 204)
