# Rest Imports
from rest_framework import status
# Local Imports
from ava_core.abstract.test import AvaCoreTest
from ava_core.evaluate.test_data import EvaluateControllerTestData, EvaluateTestTestData, EvaluateTemplateTestData, EvaluateSenderTestData, EvaluateResultTestData


# Implementation
class EvaluateControllerTest(AvaCoreTest):
    """
    EvaluateController Test
    """

    def setUp(self):
        # Make call to super.
        super(EvaluateControllerTest, self).setUp()

        # Set the data type.
        self.data = EvaluateControllerTestData
        self.data.init_requirements()

    def test_evaluate_controller_create_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure created response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.data.model.objects.count(), count + 1)
        self.assertTrue(self.does_contain_data(response.data, data))

    def test_evaluate_controller_create_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure created response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.data.model.objects.count(), count + 1)
        self.assertTrue(self.does_contain_data(response.data, data))

    def test_evaluate_controller_create_as_unauthenticated(self):
        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure unauthorized response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertEqual(self.data.model.objects.count(), count)

    def test_evaluate_controller_retrieve_single_as_user(self):
        # Create new EvaluateController models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)

        # Log in as user.
        self.login_user(self.user_user)

        # Make get request and ensure OK response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data(response.data, self.data.standard))

    def test_evaluate_controller_retrieve_all_as_user(self):
        # Create new EvaluateController models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_user)

        # Log in as user.
        self.login_user(self.user_user)

        # Make get request and ensure OK response
        response = self.client.get(self.format_url(self.data.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_list(response.data['results'], [self.data.standard, self.data.modified]))

    def test_evaluate_controller_retrieve_single_as_admin(self):
        # Create new EvaluateController models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)

        # Log in as admin.
        self.login_user(self.user_admin)

        # Make get request and ensure OK response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data(response.data, self.data.standard))

    def test_evaluate_controller_retrieve_all_as_admin(self):
        # Create new EvaluateController models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_admin)

        # Log in as admin.
        self.login_user(self.user_admin)

        # Make get request and ensure OK response
        response = self.client.get(self.format_url(self.data.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_list(response.data['results'], [self.data.standard, self.data.modified]))

    def test_evaluate_controller_retrieve_single_as_unauthorized(self):
        # Create new EvaluateController models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)

        # Make get request and ensure unauthorized response
        response = self.client.get(url)
        self.assertIn(response.status_code, self.status_forbidden)

    def test_evaluate_controller_retrieve_all_as_unauthorized(self):
        # Create new EvaluateController models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_admin)

        # Make get request and ensure unauthorized response
        response = self.client.get(self.format_url(self.data.url))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write retrieve owner tests    def test_evaluate_controller_update_exists_as_user(self):
        # Create new EvaluateController models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        # Log in as user.
        self.login_user(self.user_user)

        # Make put request and ensure OK response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_url(url, self.data.unique))

    def test_evaluate_controller_update_does_not_exist_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Make put request and ensure not found response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_controller_update_exists_as_admin(self):
        # Create new EvaluateController models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make put request and ensure OK response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_url(url, self.data.unique))

    def test_evaluate_controller_update_does_not_exist_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make put request and ensure not found response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_controller_update_exists_as_unauthorized(self):
        # Create new EvaluateController models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Make put request and ensure unauthorized response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertTrue(self.does_contain_data_url(url, self.data.standard))

    def test_evaluate_controller_update_does_not_exist_as_unauthorized(self):
        # Make put request and ensure unauthorized response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write update owner tests    def test_evaluate_controller_delete_exists_as_user(self):
        # Create new EvaluateController models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        # Log in as user.
        self.login_user(self.user_user)

        # Make delete request and ensure no content response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.data.model.objects.count(), 0)

    def test_evaluate_controller_delete_does_not_exist_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Make delete request and ensure not found response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_controller_delete_exists_as_admin(self):
        # Create new EvaluateController models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make delete request and ensure no content response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.data.model.objects.count(), 0)

    def test_evaluate_controller_delete_does_not_exist_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make delete request and ensure not found response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_controller_delete_exists_as_unauthorized(self):
        # Create new EvaluateController models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Make delete request and ensure unauthorized response
        response = self.client.get(url)
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertEqual(self.data.model.objects.count(), 1)

    def test_evaluate_controller_delete_does_not_exist_as_unauthorized(self):
        # Make delete request and ensure unauthorized response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write delete owner tests
class EvaluateTestTest(AvaCoreTest):
    """
    EvaluateTest Test
    """

    def setUp(self):
        # Make call to super.
        super(EvaluateTestTest, self).setUp()

        # Set the data type.
        self.data = EvaluateTestTestData
        self.data.init_requirements()

    def test_evaluate_test_create_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure created response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.data.model.objects.count(), count + 1)
        self.assertTrue(self.does_contain_data(response.data, data))

    def test_evaluate_test_create_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure created response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.data.model.objects.count(), count + 1)
        self.assertTrue(self.does_contain_data(response.data, data))

    def test_evaluate_test_create_as_unauthenticated(self):
        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure unauthorized response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertEqual(self.data.model.objects.count(), count)

    def test_evaluate_test_retrieve_single_as_user(self):
        # Create new EvaluateTest models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)

        # Log in as user.
        self.login_user(self.user_user)

        # Make get request and ensure OK response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data(response.data, self.data.standard))

    def test_evaluate_test_retrieve_all_as_user(self):
        # Create new EvaluateTest models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_user)

        # Log in as user.
        self.login_user(self.user_user)

        # Make get request and ensure OK response
        response = self.client.get(self.format_url(self.data.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_list(response.data['results'], [self.data.standard, self.data.modified]))

    def test_evaluate_test_retrieve_single_as_admin(self):
        # Create new EvaluateTest models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)

        # Log in as admin.
        self.login_user(self.user_admin)

        # Make get request and ensure OK response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data(response.data, self.data.standard))

    def test_evaluate_test_retrieve_all_as_admin(self):
        # Create new EvaluateTest models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_admin)

        # Log in as admin.
        self.login_user(self.user_admin)

        # Make get request and ensure OK response
        response = self.client.get(self.format_url(self.data.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_list(response.data['results'], [self.data.standard, self.data.modified]))

    def test_evaluate_test_retrieve_single_as_unauthorized(self):
        # Create new EvaluateTest models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)

        # Make get request and ensure unauthorized response
        response = self.client.get(url)
        self.assertIn(response.status_code, self.status_forbidden)

    def test_evaluate_test_retrieve_all_as_unauthorized(self):
        # Create new EvaluateTest models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_admin)

        # Make get request and ensure unauthorized response
        response = self.client.get(self.format_url(self.data.url))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write retrieve owner tests    def test_evaluate_test_update_exists_as_user(self):
        # Create new EvaluateTest models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        # Log in as user.
        self.login_user(self.user_user)

        # Make put request and ensure OK response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_url(url, self.data.unique))

    def test_evaluate_test_update_does_not_exist_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Make put request and ensure not found response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_test_update_exists_as_admin(self):
        # Create new EvaluateTest models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make put request and ensure OK response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_url(url, self.data.unique))

    def test_evaluate_test_update_does_not_exist_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make put request and ensure not found response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_test_update_exists_as_unauthorized(self):
        # Create new EvaluateTest models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Make put request and ensure unauthorized response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertTrue(self.does_contain_data_url(url, self.data.standard))

    def test_evaluate_test_update_does_not_exist_as_unauthorized(self):
        # Make put request and ensure unauthorized response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write update owner tests    def test_evaluate_test_delete_exists_as_user(self):
        # Create new EvaluateTest models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        # Log in as user.
        self.login_user(self.user_user)

        # Make delete request and ensure no content response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.data.model.objects.count(), 0)

    def test_evaluate_test_delete_does_not_exist_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Make delete request and ensure not found response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_test_delete_exists_as_admin(self):
        # Create new EvaluateTest models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make delete request and ensure no content response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.data.model.objects.count(), 0)

    def test_evaluate_test_delete_does_not_exist_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make delete request and ensure not found response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_test_delete_exists_as_unauthorized(self):
        # Create new EvaluateTest models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Make delete request and ensure unauthorized response
        response = self.client.get(url)
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertEqual(self.data.model.objects.count(), 1)

    def test_evaluate_test_delete_does_not_exist_as_unauthorized(self):
        # Make delete request and ensure unauthorized response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write delete owner tests
class EvaluateTemplateTest(AvaCoreTest):
    """
    EvaluateTemplate Test
    """

    def setUp(self):
        # Make call to super.
        super(EvaluateTemplateTest, self).setUp()

        # Set the data type.
        self.data = EvaluateTemplateTestData
        self.data.init_requirements()

    def test_evaluate_template_create_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure created response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.data.model.objects.count(), count + 1)
        self.assertTrue(self.does_contain_data(response.data, data))

    def test_evaluate_template_create_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure created response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.data.model.objects.count(), count + 1)
        self.assertTrue(self.does_contain_data(response.data, data))

    def test_evaluate_template_create_as_unauthenticated(self):
        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure unauthorized response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertEqual(self.data.model.objects.count(), count)

    def test_evaluate_template_retrieve_single_as_user(self):
        # Create new EvaluateTemplate models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)

        # Log in as user.
        self.login_user(self.user_user)

        # Make get request and ensure OK response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data(response.data, self.data.standard))

    def test_evaluate_template_retrieve_all_as_user(self):
        # Create new EvaluateTemplate models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_user)

        # Log in as user.
        self.login_user(self.user_user)

        # Make get request and ensure OK response
        response = self.client.get(self.format_url(self.data.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_list(response.data['results'], [self.data.standard, self.data.modified]))

    def test_evaluate_template_retrieve_single_as_admin(self):
        # Create new EvaluateTemplate models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)

        # Log in as admin.
        self.login_user(self.user_admin)

        # Make get request and ensure OK response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data(response.data, self.data.standard))

    def test_evaluate_template_retrieve_all_as_admin(self):
        # Create new EvaluateTemplate models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_admin)

        # Log in as admin.
        self.login_user(self.user_admin)

        # Make get request and ensure OK response
        response = self.client.get(self.format_url(self.data.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_list(response.data['results'], [self.data.standard, self.data.modified]))

    def test_evaluate_template_retrieve_single_as_unauthorized(self):
        # Create new EvaluateTemplate models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)

        # Make get request and ensure unauthorized response
        response = self.client.get(url)
        self.assertIn(response.status_code, self.status_forbidden)

    def test_evaluate_template_retrieve_all_as_unauthorized(self):
        # Create new EvaluateTemplate models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_admin)

        # Make get request and ensure unauthorized response
        response = self.client.get(self.format_url(self.data.url))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write retrieve owner tests    def test_evaluate_template_update_exists_as_user(self):
        # Create new EvaluateTemplate models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        # Log in as user.
        self.login_user(self.user_user)

        # Make put request and ensure OK response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_url(url, self.data.unique))

    def test_evaluate_template_update_does_not_exist_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Make put request and ensure not found response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_template_update_exists_as_admin(self):
        # Create new EvaluateTemplate models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make put request and ensure OK response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_url(url, self.data.unique))

    def test_evaluate_template_update_does_not_exist_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make put request and ensure not found response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_template_update_exists_as_unauthorized(self):
        # Create new EvaluateTemplate models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Make put request and ensure unauthorized response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertTrue(self.does_contain_data_url(url, self.data.standard))

    def test_evaluate_template_update_does_not_exist_as_unauthorized(self):
        # Make put request and ensure unauthorized response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write update owner tests    def test_evaluate_template_delete_exists_as_user(self):
        # Create new EvaluateTemplate models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        # Log in as user.
        self.login_user(self.user_user)

        # Make delete request and ensure no content response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.data.model.objects.count(), 0)

    def test_evaluate_template_delete_does_not_exist_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Make delete request and ensure not found response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_template_delete_exists_as_admin(self):
        # Create new EvaluateTemplate models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make delete request and ensure no content response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.data.model.objects.count(), 0)

    def test_evaluate_template_delete_does_not_exist_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make delete request and ensure not found response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_template_delete_exists_as_unauthorized(self):
        # Create new EvaluateTemplate models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Make delete request and ensure unauthorized response
        response = self.client.get(url)
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertEqual(self.data.model.objects.count(), 1)

    def test_evaluate_template_delete_does_not_exist_as_unauthorized(self):
        # Make delete request and ensure unauthorized response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write delete owner tests
class EvaluateSenderTest(AvaCoreTest):
    """
    EvaluateSender Test
    """

    def setUp(self):
        # Make call to super.
        super(EvaluateSenderTest, self).setUp()

        # Set the data type.
        self.data = EvaluateSenderTestData
        self.data.init_requirements()

    def test_evaluate_sender_create_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure created response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.data.model.objects.count(), count + 1)
        self.assertTrue(self.does_contain_data(response.data, data))

    def test_evaluate_sender_create_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure created response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.data.model.objects.count(), count + 1)
        self.assertTrue(self.does_contain_data(response.data, data))

    def test_evaluate_sender_create_as_unauthenticated(self):
        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure unauthorized response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertEqual(self.data.model.objects.count(), count)

    def test_evaluate_sender_retrieve_single_as_user(self):
        # Create new EvaluateSender models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)

        # Log in as user.
        self.login_user(self.user_user)

        # Make get request and ensure OK response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data(response.data, self.data.standard))

    def test_evaluate_sender_retrieve_all_as_user(self):
        # Create new EvaluateSender models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_user)

        # Log in as user.
        self.login_user(self.user_user)

        # Make get request and ensure OK response
        response = self.client.get(self.format_url(self.data.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_list(response.data['results'], [self.data.standard, self.data.modified]))

    def test_evaluate_sender_retrieve_single_as_admin(self):
        # Create new EvaluateSender models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)

        # Log in as admin.
        self.login_user(self.user_admin)

        # Make get request and ensure OK response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data(response.data, self.data.standard))

    def test_evaluate_sender_retrieve_all_as_admin(self):
        # Create new EvaluateSender models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_admin)

        # Log in as admin.
        self.login_user(self.user_admin)

        # Make get request and ensure OK response
        response = self.client.get(self.format_url(self.data.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_list(response.data['results'], [self.data.standard, self.data.modified]))

    def test_evaluate_sender_retrieve_single_as_unauthorized(self):
        # Create new EvaluateSender models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)

        # Make get request and ensure unauthorized response
        response = self.client.get(url)
        self.assertIn(response.status_code, self.status_forbidden)

    def test_evaluate_sender_retrieve_all_as_unauthorized(self):
        # Create new EvaluateSender models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_admin)

        # Make get request and ensure unauthorized response
        response = self.client.get(self.format_url(self.data.url))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write retrieve owner tests    def test_evaluate_sender_update_exists_as_user(self):
        # Create new EvaluateSender models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        # Log in as user.
        self.login_user(self.user_user)

        # Make put request and ensure OK response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_url(url, self.data.unique))

    def test_evaluate_sender_update_does_not_exist_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Make put request and ensure not found response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_sender_update_exists_as_admin(self):
        # Create new EvaluateSender models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make put request and ensure OK response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_url(url, self.data.unique))

    def test_evaluate_sender_update_does_not_exist_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make put request and ensure not found response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_sender_update_exists_as_unauthorized(self):
        # Create new EvaluateSender models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Make put request and ensure unauthorized response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertTrue(self.does_contain_data_url(url, self.data.standard))

    def test_evaluate_sender_update_does_not_exist_as_unauthorized(self):
        # Make put request and ensure unauthorized response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write update owner tests    def test_evaluate_sender_delete_exists_as_user(self):
        # Create new EvaluateSender models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        # Log in as user.
        self.login_user(self.user_user)

        # Make delete request and ensure no content response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.data.model.objects.count(), 0)

    def test_evaluate_sender_delete_does_not_exist_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Make delete request and ensure not found response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_sender_delete_exists_as_admin(self):
        # Create new EvaluateSender models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make delete request and ensure no content response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.data.model.objects.count(), 0)

    def test_evaluate_sender_delete_does_not_exist_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make delete request and ensure not found response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_sender_delete_exists_as_unauthorized(self):
        # Create new EvaluateSender models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Make delete request and ensure unauthorized response
        response = self.client.get(url)
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertEqual(self.data.model.objects.count(), 1)

    def test_evaluate_sender_delete_does_not_exist_as_unauthorized(self):
        # Make delete request and ensure unauthorized response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write delete owner tests
class EvaluateResultTest(AvaCoreTest):
    """
    EvaluateResult Test
    """

    def setUp(self):
        # Make call to super.
        super(EvaluateResultTest, self).setUp()

        # Set the data type.
        self.data = EvaluateResultTestData
        self.data.init_requirements()

    def test_evaluate_result_create_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure created response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.data.model.objects.count(), count + 1)
        self.assertTrue(self.does_contain_data(response.data, data))

    def test_evaluate_result_create_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure created response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.data.model.objects.count(), count + 1)
        self.assertTrue(self.does_contain_data(response.data, data))

    def test_evaluate_result_create_as_unauthenticated(self):
        # Take count.
        count = self.data.model.objects.count()

        # Store data to use.
        data = self.data.get_data('standard')

        # Make post request and ensure unauthorized response.
        response = self.client.post(self.format_url(self.data.url), data, format='json')
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertEqual(self.data.model.objects.count(), count)

    def test_evaluate_result_retrieve_single_as_user(self):
        # Create new EvaluateResult models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)

        # Log in as user.
        self.login_user(self.user_user)

        # Make get request and ensure OK response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data(response.data, self.data.standard))

    def test_evaluate_result_retrieve_all_as_user(self):
        # Create new EvaluateResult models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_user)

        # Log in as user.
        self.login_user(self.user_user)

        # Make get request and ensure OK response
        response = self.client.get(self.format_url(self.data.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_list(response.data['results'], [self.data.standard, self.data.modified]))

    def test_evaluate_result_retrieve_single_as_admin(self):
        # Create new EvaluateResult models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)

        # Log in as admin.
        self.login_user(self.user_admin)

        # Make get request and ensure OK response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data(response.data, self.data.standard))

    def test_evaluate_result_retrieve_all_as_admin(self):
        # Create new EvaluateResult models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_admin)

        # Log in as admin.
        self.login_user(self.user_admin)

        # Make get request and ensure OK response
        response = self.client.get(self.format_url(self.data.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_list(response.data['results'], [self.data.standard, self.data.modified]))

    def test_evaluate_result_retrieve_single_as_unauthorized(self):
        # Create new EvaluateResult models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)

        # Make get request and ensure unauthorized response
        response = self.client.get(url)
        self.assertIn(response.status_code, self.status_forbidden)

    def test_evaluate_result_retrieve_all_as_unauthorized(self):
        # Create new EvaluateResult models.
        self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        self.create_model_logout(self.data, data_name='modified', owner=self.user_admin)

        # Make get request and ensure unauthorized response
        response = self.client.get(self.format_url(self.data.url))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write retrieve owner tests    def test_evaluate_result_update_exists_as_user(self):
        # Create new EvaluateResult models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        # Log in as user.
        self.login_user(self.user_user)

        # Make put request and ensure OK response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_url(url, self.data.unique))

    def test_evaluate_result_update_does_not_exist_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Make put request and ensure not found response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_result_update_exists_as_admin(self):
        # Create new EvaluateResult models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make put request and ensure OK response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.does_contain_data_url(url, self.data.unique))

    def test_evaluate_result_update_does_not_exist_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make put request and ensure not found response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_result_update_exists_as_unauthorized(self):
        # Create new EvaluateResult models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Make put request and ensure unauthorized response.
        response = self.client.put(url, self.data.get_data('unique'))
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertTrue(self.does_contain_data_url(url, self.data.standard))

    def test_evaluate_result_update_does_not_exist_as_unauthorized(self):
        # Make put request and ensure unauthorized response.
        response = self.client.put(self.format_url(self.data.url + '/9999'), self.data.get_data('unique'))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write update owner tests    def test_evaluate_result_delete_exists_as_user(self):
        # Create new EvaluateResult models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_user)
        # Log in as user.
        self.login_user(self.user_user)

        # Make delete request and ensure no content response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.data.model.objects.count(), 0)

    def test_evaluate_result_delete_does_not_exist_as_user(self):
        # Log in as user.
        self.login_user(self.user_user)

        # Make delete request and ensure not found response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_result_delete_exists_as_admin(self):
        # Create new EvaluateResult models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make delete request and ensure no content response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.data.model.objects.count(), 0)

    def test_evaluate_result_delete_does_not_exist_as_admin(self):
        # Log in as admin.
        self.login_user(self.user_admin)

        # Make delete request and ensure not found response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_evaluate_result_delete_exists_as_unauthorized(self):
        # Create new EvaluateResult models, storing URL.
        url = self.create_model_logout(self.data, data_name='standard', owner=self.user_admin)
        # Make delete request and ensure unauthorized response
        response = self.client.get(url)
        self.assertIn(response.status_code, self.status_forbidden)
        self.assertEqual(self.data.model.objects.count(), 1)

    def test_evaluate_result_delete_does_not_exist_as_unauthorized(self):
        # Make delete request and ensure unauthorized response
        response = self.client.get(self.format_url(self.data.url + '/9999'))
        self.assertIn(response.status_code, self.status_forbidden)

    # TODO:    Write delete owner tests

