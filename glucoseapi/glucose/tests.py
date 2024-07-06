from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from glucose.models import GlucoseLevel, GlucoseLevelMetadata

class GlucoseLevelTests(APITestCase):
    """
    Test case class for testing the GlucoseLevel API endpoints.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user and corresponding glucose level metadata,
        as well as creating glucose levels for the user.
        """
        # Create a user and corresponding glucose level metadata
        self.user_metadata = GlucoseLevelMetadata.objects.create(
            user_id="test_user",
            created_at="2024-07-01T00:00:00Z",
            created_by="test_creator"
        )
        
        # Create glucose levels for the user
        self.glucose_level1 = GlucoseLevel.objects.create(
            metadata=self.user_metadata,
            device="Device1",
            serial_number="12345",
            device_timestamp="2024-07-01T12:00:00Z",
            recording_type="Type1"
        )
        
        self.glucose_level2 = GlucoseLevel.objects.create(
            metadata=self.user_metadata,
            device="Device2",
            serial_number="67890",
            device_timestamp="2024-07-02T12:00:00Z",
            recording_type="Type2"
        )

    def test_get_levels_by_user_id(self):
        """
        Test case for getting glucose levels by user ID.

        This test sends a GET request to the 'get_levels_by_user_id' endpoint
        with a specific user ID and checks if the response status code is 200 OK
        and the number of results in the response data is 2.

        """
        url = reverse('get_levels_by_user_id')
        response = self.client.get(url, {'user_id': 'test_user'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_levels_by_user_id_missing_param(self):
        """
        Test case to check if the 'get_levels_by_user_id' API returns a 400 BAD REQUEST
        when the 'user_id' parameter is missing.
        """
        url = reverse('get_levels_by_user_id')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "user_id parameter is required")

    def test_get_levels_by_user_id_non_existent_user(self):
        """
        Test case to verify the behavior when attempting to get glucose levels for a non-existent user.

        This test sends a GET request to the 'get_levels_by_user_id' endpoint with a non-existent user ID.
        It then checks that the response status code is 500 (Internal Server Error) and that the error message
        contains the expected error message "User is not found".

        This test ensures that the API handles the scenario of requesting glucose levels for a user that does not exist.

        """
        url = reverse('get_levels_by_user_id')
        response = self.client.get(url, {'user_id': 'non_existent_user'})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("User is not found", response.data['error'])

    def test_get_level_by_id(self):
        """
        Test case for retrieving a glucose level by its ID.

        This method sends a GET request to the 'get_level_by_id' endpoint with the ID of a glucose level.
        It then asserts that the response status code is 200 (OK) and that the returned data has the correct ID.

        """
        url = reverse('get_level_by_id', args=[self.glucose_level1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.glucose_level1.id)

    def test_get_level_by_id_non_existent(self):
        """
        Test case to verify the behavior when trying to get a non-existent glucose level by ID.
        """
        url = reverse('get_level_by_id', args=[99999999999999999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Glucose level with given ID not found")

