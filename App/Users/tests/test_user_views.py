import json

from django_rest_passwordreset.models import ResetPasswordToken

from Users.factories.user_factories import UserFactory
from Users.tests.abstract_test_classes import UsersAbstractUtils
from Users.models import User

ENDPOINT = '/api/v1/users'


class UserCreateTest(UsersAbstractUtils):
    def test_create_user_fails_with_an_used_email(self):
        UserFactory(email='emailused@appname.me')
        data = {
            'first_name': 'Test',
            'last_name': 'Tested',
            'email': 'emailused@appname.me',
            'password': 'password',
            'password_confirmation': 'password',
        }
        response = self.client.post(f'{ENDPOINT}/signup/', data, format='json')
        message_one = 'email'
        message_two = 'This field must be unique'
        self.assertEqual(response.status_code, 400)
        self.assertTrue(message_one in response.data)
        self.assertTrue(message_two in response.data['email'][0])

    def test_create_user_fails_with_a_common_password(self):
        data = {
            'first_name': 'Test',
            'last_name': 'Tested',
            'email': 'unusedemail@appname.me',
            'password': 'password',
            'password_confirmation': 'password',
        }
        response = self.client.post(f'{ENDPOINT}/signup/', data, format='json')
        message = 'This password is too common.'
        self.assertEqual(response.status_code, 400)
        self.assertTrue(message in response.data['non_field_errors'][0])

    def test_create_user_is_successfull(self):
        data = {
            'first_name': 'Test',
            'last_name': 'Tested',
            'email': 'unusedemail@appname.me',
            'password': 'strongpassword',
            'password_confirmation': 'strongpassword',
        }
        # Normal and admin user already in database
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(f'{ENDPOINT}/signup/', data, format='json')
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['phone_number'], '')
        self.assertEqual(response.data['is_verified'], False)
        self.assertEqual(response.data['is_admin'], False)
        self.assertEqual(response.data['is_premium'], False)

    def test_sign_up_is_successfull_but_do_not_create_an_user_with_special_fields_modified(
        self,
    ):
        data = {
            'first_name': 'Test',
            'last_name': 'Tested',
            'email': 'unusedemail2@appname.me',
            'password': 'strongpassword',
            'password_confirmation': 'strongpassword',
            'phone_number': '+03999999999',
            'is_verified': True,
            'is_admin': True,
            'is_premium': True,
        }
        # Normal and admin user already in database
        self.assertEqual(User.objects.count(), 2)
        response = self.client.post(f'{ENDPOINT}/signup/', data, format='json')
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['phone_number'], '')
        self.assertEqual(response.data['is_verified'], False)
        self.assertEqual(response.data['is_admin'], False)
        self.assertEqual(response.data['is_premium'], False)


class UserLogInTest(UsersAbstractUtils):
    def test_login_fails_with_wrong_email(self):
        data = {'email': 'wroongemail@appname.me', 'password': 'RightPassword'}
        response = self.client.post(f'{ENDPOINT}/login/', data, format='json')
        message = 'Invalid credentials'
        self.assertEqual(response.status_code, 400)
        self.assertTrue(message in response.data['non_field_errors'][0])

    def test_login_fails_with_wrong_password(self):
        UserFactory(email='rightemail@appname.me', password='RightPassword')
        data = {'email': 'rightemail@appname.me', 'password': 'WrongPassword'}
        response = self.client.post(f'{ENDPOINT}/login/', data, format='json')
        message = 'Invalid credentials'
        self.assertEqual(response.status_code, 400)
        self.assertTrue(message in response.data['non_field_errors'][0])

    def test_login_fails_with_user_not_verified(self):
        UserFactory(email='rightemail@appname.me', password='RightPassword')
        data = {'email': 'rightemail@appname.me', 'password': 'RightPassword'}
        response = self.client.post(f'{ENDPOINT}/login/', data, format='json')
        message = 'User is not verified'
        self.assertEqual(response.status_code, 400)
        self.assertTrue(message in response.data['non_field_errors'][0])

    def test_log_in_is_successful_with_a_verified_user(self):
        testing_user = UserFactory(email='rightemail@appname.me', password='RightPassword')
        testing_user.is_verified = True
        testing_user.save()
        data = {'email': 'rightemail@appname.me', 'password': 'RightPassword'}
        response = self.client.post(f'{ENDPOINT}/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('token' in data)
        self.assertTrue('user' in data)
        self.assertEqual(data['user']['first_name'], testing_user.first_name)
        self.assertEqual(data['user']['last_name'], testing_user.last_name)
        self.assertEqual(data['user']['email'], testing_user.email)


class UserListTests(UsersAbstractUtils):
    def test_list_users_fails_as_an_unauthenticated_user(self):
        response = self.client.get(f'{ENDPOINT}/', format='json')
        self.assertEqual(response.status_code, 401)

    def test_list_users_fails_as_an_authenticated_unverified_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(f'{ENDPOINT}/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_list_users_fails_as_an_authenticated_verified_normal_user(self):
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(f'{ENDPOINT}/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_list_users_is_successful_as_an_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'{ENDPOINT}/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


class UserGetTests(UsersAbstractUtils):
    def test_get_user_fails_as_an_unauthenticated_user(self):
        response = self.client.get(f'{ENDPOINT}/{self.normal_user.id}/', format='json')
        self.assertEqual(response.status_code, 401)

    def test_get_user_fails_as_an_authenticated_unverified_user(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(f'{ENDPOINT}/{self.normal_user.id}/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_get_user_fails_as_an_authenticated_verified_user_to_other_users_data(self):
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(f'{ENDPOINT}/{self.admin_user.id}/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_get_user_is_successful_as_an_authenticated_verified_user_to_its_data(self):
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(f'{ENDPOINT}/{self.normal_user.id}/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.normal_user.id)
        self.assertEqual(response.data['email'], self.normal_user.email)

    def test_get_user_is_successful_to_other_users_data_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'{ENDPOINT}/{self.normal_user.id}/', format='json')
        self.assertEqual(response.status_code, 200)


class UserUpdateTest(UsersAbstractUtils):
    def test_update_user_fails_as_an_unauthenticated_user(self):
        data = {
            'first_name': 'Test edited',
            'last_name': 'Tested Edit',
            'email': 'edituser2@appname.me',
            'phone_number': '+32987654321',
            'old_password': 'password',
            'password': 'NewPassword95',
        }
        response = self.client.put(f'{ENDPOINT}/{self.normal_user.id}/', data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_update_user_fails_as_an_authenticated_unverified_user(self):
        data = {
            'first_name': 'Test edited',
            'last_name': 'Tested Edit',
            'email': 'edituser2@appname.me',
            'phone_number': '+32987654321',
            'old_password': 'password',
            'password': 'NewPassword95',
        }
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.put(f'{ENDPOINT}/{self.normal_user.id}/', data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_update_user_fails_as_an_authenticated_verified_user_to_other_users_data(self):
        data = {
            'first_name': 'Test edited',
            'last_name': 'Tested Edit',
            'email': 'edituser2@appname.me',
            'phone_number': '+32987654321',
            'old_password': 'password',
            'password': 'NewPassword95',
        }
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.put(f'{ENDPOINT}/{self.admin_user.id}/', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(self.normal_user.email, data['email'])

    def test_update_user_is_successful_as_an_authenticated_verified_user_to_its_data(self):
        data = {
            'first_name': 'Test edited',
            'last_name': 'Tested Edit',
            'email': 'edituser2@appname.me',
            'phone_number': '+32987654321',
            'old_password': 'password',
            'password': 'NewPassword95',
        }
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.put(f'{ENDPOINT}/{self.normal_user.id}/', data, format='json')
        self.assertEqual(response.status_code, 202)
        self.normal_user = User.objects.get(id=self.normal_user.id)
        self.assertEqual(self.normal_user.email, data['email'])
        self.assertEqual(self.normal_user.phone_number, data['phone_number'])
        self.assertEqual(self.normal_user.first_name, data['first_name'])
        self.assertEqual(self.normal_user.last_name, data['last_name'])
        self.assertTrue(self.normal_user.check_password(data['password']))

    def test_update_user_fails_as_an_authenticated_verified_user_with_an_used_email(self):
        UserFactory(email='emailused@appname.me')
        data = {
            'first_name': 'Test',
            'last_name': 'Tested',
            'email': 'emailused@appname.me',
            'password': 'password',
        }
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.put(f'{ENDPOINT}/{self.normal_user.id}/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Email is taken' in response.data)

    def test_update_user_fails_as_an_authenticated_verified_user_with_an_used_phone_number(
        self,
    ):
        UserFactory(phone_number='+03999999999')
        data = {
            'first_name': 'Test',
            'last_name': 'Tested',
            'email': 'edituser3@appname.me',
            'password': 'password',
            'phone_number': '+03999999999',
        }
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.put(f'{ENDPOINT}/{self.normal_user.id}/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Phone number is taken' in response.data)

    def test_update_user_fails_as_an_authenticated_verified_user_with_a_wrong_old_password(
        self,
    ):
        data = {
            'first_name': 'Test',
            'last_name': 'Tested',
            'email': 'finalemail@appname.me',
            'phone_number': '+32987654321',
            'old_password': 'NewPassword95 wrong',
            'password': 'This is a password',
        }
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.put(f'{ENDPOINT}/{self.normal_user.id}/', data, format='json')
        message = 'Wrong password'
        self.assertEqual(response.status_code, 400)
        self.assertTrue(message in response.data)

    def test_update_user_fails_as_an_authenticated_verified_user_without_old_password(self):
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.normal_user)
        data = {
            'first_name': 'Test',
            'last_name': 'Tested',
            'email': 'finalemail@appname.me',
            'phone_number': '+32987654321',
            'password': 'This is a password',
        }
        response = self.client.put(f'{ENDPOINT}/{self.normal_user.id}/', data, format='json')
        message = 'Old password is required to set a new one'
        self.assertEqual(response.status_code, 400)
        self.assertTrue(message in response.data)

    def test_update_user_is_successful_as_an_authenticated_verified_user_with_just_a_new_password(
        self,
    ):
        data = {'old_password': 'password', 'password': 'New Password'}
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.put(f'{ENDPOINT}/{self.normal_user.id}/', data, format='json')
        self.assertEqual(response.status_code, 202)
        self.normal_user = User.objects.get(id=self.normal_user.id)
        self.assertTrue(self.normal_user.check_password(data['password']))

    def test_update_user_is_successful_as_an_authenticated_verified_user_but_do_not_change_special_fields(
        self,
    ):
        data = {
            'first_name': 'Test',
            'last_name': 'Tested',
            'email': 'emailemail@appname.me',
            'phone_number': '+32987654321',
            'old_password': 'password',
            'password': 'New password',
            'is_verified': False,
            'is_admin': True,
            'is_premium': True,
        }
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.put(f'{ENDPOINT}/{self.normal_user.id}/', data, format='json')
        self.assertEqual(response.status_code, 202)
        self.normal_user = User.objects.get(id=self.normal_user.id)
        self.assertEqual(self.normal_user.email, data['email'])
        self.assertEqual(self.normal_user.phone_number, data['phone_number'])
        self.assertEqual(self.normal_user.first_name, data['first_name'])
        self.assertEqual(self.normal_user.last_name, data['last_name'])
        self.assertTrue(self.normal_user.check_password(data['password']))
        self.assertEqual(self.normal_user.is_verified, True)
        self.assertEqual(self.normal_user.is_admin, False)
        self.assertEqual(self.normal_user.is_premium, False)

    def test_update_user_is_successful_as_admin_to_other_user_data_but_do_not_change_special_fields(
        self,
    ):
        data = {
            'first_name': 'Test',
            'last_name': 'Tested',
            'email': 'emailemail@appname.me',
            'phone_number': '+32987654321',
            'old_password': 'password',
            'password': 'New password',
            'is_verified': False,
            'is_admin': True,
            'is_premium': True,
        }
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(f'{ENDPOINT}/{self.normal_user.id}/', data, format='json')
        self.assertEqual(response.status_code, 202)
        self.normal_user = User.objects.get(id=self.normal_user.id)
        self.assertEqual(self.normal_user.email, data['email'])
        self.assertEqual(self.normal_user.phone_number, data['phone_number'])
        self.assertEqual(self.normal_user.first_name, data['first_name'])
        self.assertEqual(self.normal_user.last_name, data['last_name'])
        self.assertTrue(self.normal_user.check_password(data['password']))
        self.assertEqual(self.normal_user.is_verified, True)
        self.assertEqual(self.normal_user.is_admin, False)
        self.assertEqual(self.normal_user.is_premium, False)


class UserDeleteTests(UsersAbstractUtils):
    def test_delete_user_fails_as_an_unauthenticated_user(self):
        self.assertEqual(User.objects.count(), 2)
        response = self.client.delete(f'{ENDPOINT}/{self.normal_user.id}/', format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(User.objects.count(), 2)

    def test_delete_user_fails_as_an_authenticated_unverified_user_to_its_data(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.delete(f'{ENDPOINT}/{self.normal_user.id}/', format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(User.objects.count(), 2)

    def test_delete_user_fails_as_an_authenticated_verified_user_to_to_other_users_data(self):
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.delete(f'{ENDPOINT}/{self.admin_user.id}/', format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(User.objects.count(), 2)

    def test_delete_user_is_successful_as_an_authenticated_verified_user_to_its_data(self):
        self.normal_user.is_verified = True
        self.normal_user.save()
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.delete(f'{ENDPOINT}/{self.normal_user.id}/', format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 1)

    def test_delete_user_is_successful_as_admin_to_other_users_data(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'{ENDPOINT}/{self.normal_user.id}/', format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 1)


class UserVerifyTests(UsersAbstractUtils):
    def test_verify_user(self):
        # Test that any user can verify its user with a get
        # request with it id and token
        token = self.normal_user.generate_verification_token()
        self.assertEqual(self.normal_user.is_verified, False)
        response = self.client.get(f'{ENDPOINT}/{self.normal_user.id}/verify/?token={token}')
        self.assertEqual(response.status_code, 202)
        normal_user_updated = User.objects.get(id=self.normal_user.id)
        self.assertEqual(normal_user_updated.is_verified, True)


class UserPasswordResetTests(UsersAbstractUtils):
    def test_reset_password(self):
        # Test that any user can reset its password via API
        self.assertTrue(self.normal_user.check_password('password'))
        response = self.client.post(
            f'/api/v1/password_reset/', {'email': self.normal_user.email}
        )
        self.assertEqual(response.status_code, 200)
        tokens = ResetPasswordToken.objects.all()
        self.assertEqual(len(tokens), 1)
        token = tokens[0].key
        data = {'token': token, 'password': 'NewPassword95'}
        self.client.post(f'/api/v1/password_reset/confirm/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.normal_user = User.objects.get(id=self.normal_user.id)
        self.assertTrue(self.normal_user.check_password('NewPassword95'))
