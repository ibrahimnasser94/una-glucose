import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from glucose.models import GlucoseLevel, GlucoseLevelMetadata
from glucose.serializers import GlucoseLevelMetadataSerializer, GlucoseLevelSerializer
from glucose.dtos import GlucoseLevelDTO

# Create your views here.
@api_view(['GET'])
def get_levels_by_user_id(request):
    """
    Retrieve glucose levels for a specific user based on user_id.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The HTTP response containing the serialized glucose levels.

    Raises:
        Exception: If an error occurs during the retrieval process.
    """
    try:
        user_id, limit, sort_param = get_request_params(request)
        if user_id is None:
            return Response({"error": "user_id parameter is required"}, status=400)
        paginator, result_page = get_filtered_levels(request, user_id, limit, sort_param)  
        if result_page is not None:
            serializer = GlucoseLevelSerializer(result_page, many=True)
        if paginator is not None:
            return paginator.get_paginated_response(serializer.data)
    except Exception as ex:
        return Response({"error": repr(ex)}, status=500)

@api_view(['GET'])
def get_level_by_id(request, id):
    """
    Retrieve a glucose level by its ID.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the glucose level to retrieve.

    Returns:
        Response: The HTTP response containing the serialized glucose level data.

    Raises:
        Exception: If an error occurs while retrieving the glucose level.

    """
    try:
        level = GlucoseLevel.objects.filter(id=id).first()
        if level is not None:
            serializer = GlucoseLevelSerializer(level)
            return Response(serializer.data)
        else:
            return Response("Glucose level with given ID not found", status=404)
    except Exception as ex:
        return Response({"error": repr(ex)}, status=500)

def get_request_params(request):
    """
    Get the request parameters from the given request object.

    Args:
        request (HttpRequest): The request object.

    Returns:
        tuple: A tuple containing the user_id, limit, and sort_param extracted from the request query parameters.
    """
    user_id = request.query_params.get('user_id')
    limit = request.query_params.get('limit')
    sort_param = request.query_params.get('sort_by')
    return user_id, limit, sort_param

def get_filtered_levels(request, user_id, limit, sort_param):
    """
    Retrieve filtered glucose levels for a specific user.

    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The ID of the user.
        limit (int): The maximum number of levels to retrieve.
        sort_param (str): The parameter to sort the levels by.

    Returns:
        tuple: A tuple containing the paginator object and the paginated result page.

    Raises:
        ValueError: If the user is not found.
    """
    user = GlucoseLevelMetadata.objects.filter(user_id=user_id)
    if user.exists():
        user = user.first()
        levels = GlucoseLevel.objects.filter(metadata=user)
        if sort_param is not None:
            levels = levels.order_by(sort_param)
        paginator = create_paginator(limit)
        result_page = paginator.paginate_queryset(levels, request)
        return paginator, result_page
    raise ValueError('User is not found')

def create_paginator(limit):
    """
    Creates a paginator object with the specified limit.

    Args:
        limit (int): The maximum number of items per page.

    Returns:
        paginator (PageNumberPagination): The paginator object with the specified limit.
    """
    paginator = PageNumberPagination()
    if limit is not None:
        paginator.page_size = limit
    return paginator

@api_view(['POST'])
def create_levels(request):
    """
    API endpoint for creating glucose levels.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The HTTP response object containing the serialized metadata and glucose levels.

    Raises:
        Exception: If an error occurs during the processing of glucose levels.

    """
    try:
        levels = json.loads(request.body)
        if levels:
            metadata_objects, glucose_level_objects = process_glucose_levels(levels)
            serialized_metadata = GlucoseLevelMetadataSerializer(metadata_objects, many=True)
            serialized_glucose_levels = GlucoseLevelSerializer(glucose_level_objects, many=True)
            return Response({"metadata": serialized_metadata.data, "glucose_levels": serialized_glucose_levels.data})
        else:
            return Response("No object returned in body", status=400)
    except Exception as ex:
        return Response({"error": repr(ex)}, status=500)

def process_glucose_levels(levels):
    """
    Process a list of glucose levels.

    Args:
        levels (list): A list of glucose level dictionaries.

    Returns:
        tuple: A tuple containing two lists - metadata_objects and glucose_level_objects.
            metadata_objects (list): A list of metadata objects created or updated for each glucose level.
            glucose_level_objects (list): A list of glucose level objects created or updated.

    """
    metadata_objects = []
    glucose_level_objects = []
    for level in levels:
        dto = GlucoseLevelDTO.from_dict(level)
        metadata, glucose_level = create_or_update_glucose_level(dto)
        metadata_objects.append(metadata)
        glucose_level_objects.append(glucose_level)
    return metadata_objects, glucose_level_objects

def create_or_update_glucose_level(dto):
    """
    Creates or updates a glucose level record in the database.

    Args:
        dto: The data transfer object containing the glucose level information.

    Returns:
        A tuple containing the metadata and glucose level objects.

    """
    metadata, created = GlucoseLevelMetadata.objects.update_or_create(
        user_id=dto.user_id,
        defaults={
            'created_at': dto.created_at,
            'created_by': dto.created_by,
        }
    )

    # Create or update the glucose level
    glucose_level, created = GlucoseLevel.objects.update_or_create(
        metadata=metadata,
        device=dto.device,
        serial_number=dto.serial_number,
        device_timestamp=dto.device_timestamp,
        defaults={
            'recording_type': dto.recording_type,
            'glucose_value_trend': dto.glucose_value_trend,
            'glucose_scan': dto.glucose_scan,
            'non_numerical_rapid_acting_insulin': dto.non_numerical_rapid_acting_insulin,
            'rapid_acting_insulin': dto.rapid_acting_insulin,
            'non_numerical_nutritional_data': dto.non_numerical_nutritional_data,
            'carbohydrates_grams': dto.carbohydrates_grams,
            'carbohydrates_portions': dto.carbohydrates_portions,
            'non_numerical_depot_insulin': dto.non_numerical_depot_insulin,
            'depot_insulin': dto.depot_insulin,
            'notes': dto.notes,
            'glucose_test_strips': dto.glucose_test_strips,
            'ketone': dto.ketone,
            'mealtime_insulin': dto.mealtime_insulin,
            'correction_insulin': dto.correction_insulin,
            'insulin_change_by_user': dto.insulin_change_by_user,
        }
    )
    
    return metadata, glucose_level
