from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from requests.auth import HTTPBasicAuth
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User, Photo
from django.contrib.auth.models import User as Admin
import base64

HOST = 'http://localhost:8000'
UNAME = 'test_root'
TEST_USER = Admin.objects.get(username=UNAME)
SAMPLE_IMG_PATH = r'/home/marko/Projects/faks/RZNU/lab1_rest/media/photos/sample.png'

def resolve(path):
    if not path.startswith('/'): 
        path = '/' + path
    if not path.endswith('/'): 
        path += '/'

    return HOST + path

class UserTests(APITestCase):

    def login(self):
        self.client.force_authenticate(TEST_USER)

    def logout(self):
        self.client.force_authenticate()

    def make_test_user(self, data={'name': 'TestingUser', 'email': 'test@test.com'}):
        url = resolve('/api/users/')
        self.login()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.logout()
        return response

    def test_get_users(self):
        url = resolve('/api/users/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_user(self):
        self.make_test_user()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'TestingUser')


    def test_create_users(self):
        self.make_test_user(data={'name': 'TestingUser', 'email': 'test@test.com'})
        self.make_test_user(data={'name': 'TestingUser2', 'email': 'test@test.com'})
  

        self.assertEqual(User.objects.count(), 2)
        users = User.objects.all()
        self.assertEqual(users[0].name, 'TestingUser')
        self.assertEqual(users[1].name, 'TestingUser2')
        self.logout()



    def test_get_single_user(self):
        self.make_test_user()
        url = resolve('/api/users/1/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_single_user(self):
        self.make_test_user()
        self.assertEqual(User.objects.count(), 1)

        url = resolve('/api/users/1/')
        data = {'name': 'TestingUserUpdated', 'email': 'test@test.com'}

        self.login()
        response = self.client.put(url, data, format='json')
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'TestingUserUpdated')


    def test_delete_user(self):
        self.make_test_user()
        self.assertEqual(User.objects.count(), 1)

        url = resolve('/api/users/1/')

        self.login()
        response = self.client.delete(url, format='json')
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)


    def test_create_user_not_autorized(self):
        url = resolve('/api/users/')
        data = {'name': 'TestingUser', 'email': 'test@test.com'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_not_autorized(self):
        self.make_test_user()
        self.assertEqual(User.objects.count(), 1)

        url = resolve('/api/users/1/')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_single_user_not_autorized(self):
        self.make_test_user()
        self.assertEqual(User.objects.count(), 1)

        url = resolve('/api/users/1/')
        data = {'name': 'TestingUserUpdated', 'email': 'test@test.com'}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class PhotoTests(APITestCase):

    def login(self):
        self.client.force_authenticate(TEST_USER)

    def logout(self):
        self.client.force_authenticate()

    def make_test_user(self, data={'name': 'TestingUser', 'email': 'test@test.com'}):
        url = resolve('/api/users/')
        self.login()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.logout()
        return response

    def load_sample_image(self):
        with open(SAMPLE_IMG_PATH, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string

    def make_test_photo(self, user_id=1, title='sample image'):
        data={'user': user_id, 'title': title, 'image': self.load_sample_image()}
        url = resolve('/api/photos/')

        self.login()
        response = self.client.post(url, data, format='json')
        self.logout()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response

    def delete_photo(self, id=1):
        url = resolve('/api/photos/1/')
        self.login()
        response = self.client.delete(url, format='json')
        self.logout()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_get_photos(self):
        url = resolve('/api/photos/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_photo(self):
        self.make_test_user()
        title = 'sample img'
        response = self.make_test_photo(1, title)
        self.assertEqual(Photo.objects.count(), 1)
        self.assertEqual(Photo.objects.get().title, title)
        self.assertEqual(Photo.objects.get().user.id, 1)

        self.delete_photo()

    def test_get_single_photo(self):
        self.make_test_user()
        self.make_test_photo()

        url = resolve('/api/photos/1/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.delete_photo()


    def test_update_single_photo(self):
        self.make_test_user()
        self.make_test_photo(title='sampleImage')
        self.assertEqual(Photo.objects.count(), 1)
        self.assertEqual(Photo.objects.get().title, 'sampleImage')



        url = resolve('/api/photos/1/')
        data={'user': 1, 'title': 'new title', 'image': self.load_sample_image()}


        self.login()
        response = self.client.put(url, data, format='json')
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Photo.objects.count(), 1)
        self.assertEqual(Photo.objects.get().title, 'new title')
        self.delete_photo()


    def test_delete_photo(self):
        self.make_test_user()
        self.make_test_photo()
        self.assertEqual(Photo.objects.count(), 1)

        url = resolve('/api/photos/1/')

        self.login()
        response = self.client.delete(url, format='json')
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Photo.objects.count(), 0)


    def test_create_photo_not_autorized(self):
        url = resolve('/api/photos/')
        data={'user': 1, 'title': 'sample_image', 'image': self.load_sample_image()}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_photo_not_autorized(self):
        self.make_test_user()
        self.make_test_photo()
        self.assertEqual(User.objects.count(), 1)

        url = resolve('/api/photos/1/')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.delete_photo()

    def test_update_single_photo_not_autorized(self):
        self.make_test_user()
        self.make_test_photo()
        self.assertEqual(Photo.objects.count(), 1)

        url = resolve('/api/photos/1/')
        data={'user': 1, 'title': 'new_title', 'image': self.load_sample_image()}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.delete_photo()




