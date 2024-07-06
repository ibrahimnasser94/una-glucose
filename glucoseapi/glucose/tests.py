from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from glucose.models import GlucoseLevel, GlucoseLevelMetadata
from glucose.dtos import GlucoseLevelDTO
from glucose.views import create_or_update_glucose_level
from glucose.serializers import GlucoseLevelMetadataSerializer, GlucoseLevelSerializer

class GlucoseLevelTests(APITestCase):
    """
    Test case class for testing the GlucoseLevel API endpoints. Data Transfer Object for Glucose Level. Partially generated with Github Copilot.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user and corresponding glucose level metadata,
        as well as creating glucose levels for the user.
        """
        # Create a user and corresponding glucose level metadata
        self.client = APIClient()
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

    def test_create_or_update_glucose_level(self):
        """
        Test case for the create_or_update_glucose_level function.

        This test verifies that the create_or_update_glucose_level function correctly creates or updates a GlucoseLevelDTO object.

        It does the following:
        - Creates a GlucoseLevelDTO object for testing.
        - Calls the create_or_update_glucose_level function with the DTO object.
        - Asserts that the GlucoseLevelMetadata object is created or updated correctly.
        - Asserts that the GlucoseLevel object is created or updated correctly.
        """

        # Create a GlucoseLevelDTO object for testing
        dto = GlucoseLevelDTO(
            user_id=1,
            created_at='2022-01-01 12:00:00',
            created_by='John Doe',
            device='Device A',
            serial_number='123456',
            device_timestamp='2022-01-01 12:00:00',
            recording_type='Type A',
            glucose_value_trend='Trend A',
            glucose_scan='Scan A',
            non_numerical_rapid_acting_insulin='Insulin A',
            rapid_acting_insulin=10,
            non_numerical_nutritional_data='Data A',
            carbohydrates_grams=50,
            carbohydrates_portions=2,
            non_numerical_depot_insulin='Insulin B',
            depot_insulin=20,
            notes='Note A',
            glucose_test_strips='Strips A',
            ketone='Ketone A',
            mealtime_insulin=30,
            correction_insulin=40,
            insulin_change_by_user=50
        )

        # Call the create_or_update_glucose_level function
        metadata, glucose_level = create_or_update_glucose_level(dto)

        # Assert that the GlucoseLevelMetadata object is created or updated correctly
        assert metadata.user_id == 1
        assert metadata.created_at == '2022-01-01 12:00:00'
        assert metadata.created_by == 'John Doe'

        # Assert that the GlucoseLevel object is created or updated correctly
        assert glucose_level.metadata == metadata
        assert glucose_level.device == 'Device A'
        assert glucose_level.serial_number == '123456'
        assert glucose_level.device_timestamp == '2022-01-01 12:00:00'
        assert glucose_level.recording_type == 'Type A'
        assert glucose_level.glucose_value_trend == 'Trend A'
        assert glucose_level.glucose_scan == 'Scan A'
        assert glucose_level.non_numerical_rapid_acting_insulin == 'Insulin A'
        assert glucose_level.rapid_acting_insulin == 10
        assert glucose_level.non_numerical_nutritional_data == 'Data A'
        assert glucose_level.carbohydrates_grams == 50
        assert glucose_level.carbohydrates_portions == 2
        assert glucose_level.non_numerical_depot_insulin == 'Insulin B'
        assert glucose_level.depot_insulin == 20
        assert glucose_level.notes == 'Note A'
        assert glucose_level.glucose_test_strips == 'Strips A'
        assert glucose_level.ketone == 'Ketone A'
        assert glucose_level.mealtime_insulin == 30
        assert glucose_level.correction_insulin == 40
        assert glucose_level.insulin_change_by_user == 50

    def test_create_levels_success(self):
        """
        Test case to verify the successful creation of glucose levels.

        This test case prepares test data for two glucose level records and makes a POST request to the 'create_levels' endpoint.
        It then asserts that the response status code is 200, indicating a successful creation.

        Test data:
        - Two glucose level records with different attributes such as user ID, device, glucose value, insulin values, etc.

        Steps:
        1. Prepare the test data by defining a list of glucose level records.
        2. Make a POST request to the 'create_levels' endpoint with the test data.
        3. Assert that the response status code is 200.

        """
        # Prepare test data
        levels = [
            {
                "user_id": "user123",
                "created_at": "2024-07-06T12:34:56",
                "created_by": "doctor_jane",
                "device": "Accu-Chek Guide",
                "serial_number": "SN12345678",
                "device_timestamp": "2024-07-06T12:00:00",
                "recording_type": "fasting",
                "glucose_value_trend": "stable",
                "glucose_scan": "105",
                "non_numerical_rapid_acting_insulin": "none",
                "rapid_acting_insulin": "0",
                "non_numerical_nutritional_data": "none",
                "carbohydrates_grams": "50",
                "carbohydrates_portions": "1",
                "non_numerical_depot_insulin": "none",
                "depot_insulin": "0",
                "notes": "Morning reading",
                "glucose_test_strips": "105",
                "ketone": "0.1",
                "mealtime_insulin": "0",
                "correction_insulin": "0",
                "insulin_change_by_user": "0"
            },
            {
                "user_id": "user456",
                "created_at": "2024-07-06T18:45:00",
                "created_by": "nurse_john",
                "device": "Freestyle Libre",
                "serial_number": "SN87654321",
                "device_timestamp": "2024-07-06T18:30:00",
                "recording_type": "postprandial",
                "glucose_value_trend": "rising",
                "glucose_scan": "140",
                "non_numerical_rapid_acting_insulin": "none",
                "rapid_acting_insulin": "5",
                "non_numerical_nutritional_data": "none",
                "carbohydrates_grams": "60",
                "carbohydrates_portions": "2",
                "non_numerical_depot_insulin": "none",
                "depot_insulin": "10",
                "notes": "After lunch",
                "glucose_test_strips": "140",
                "ketone": "0.2",
                "mealtime_insulin": "5",
                "correction_insulin": "2",
                "insulin_change_by_user": "0"
            }
        ]

        # Make POST request to create levels
        response = self.client.post(reverse("create_levels"), data=levels, format="json")

        # Assert response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_levels_no_data(self):
        """
        Test case for creating glucose levels without any data.

        This test case makes a POST request to the 'create_levels' endpoint without providing any data.
        It then asserts that the response status code is 400 (Bad Request) and the response data is "No object returned in body".
        """
        # Make POST request without any data
        response = self.client.post(reverse("create_levels"), data=[], format="json")

        # Assert response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert response data
        self.assertEqual(response.data, "No object returned in body")

    def test_create_levels_error(self):
        """
        Test case to verify the behavior of the create_levels API endpoint when invalid data is provided.

        This test makes a POST request to the create_levels endpoint with invalid data and asserts that the response
        status code is 500 (Internal Server Error) and that the response data contains an "error" key.

        """
        # Make POST request with invalid data
        response = self.client.post(reverse("create_levels"), data="invalid_data", format="json")

        # Assert response status code
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Assert response data
        self.assertIn("error", response.data)

