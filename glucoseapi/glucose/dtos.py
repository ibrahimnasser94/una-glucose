from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class GlucoseLevelDTO:
    """Data Transfer Object for Glucose Level. Generated with ChatGPT 4o."""

    # GlucoseLevelMetadata fields
    user_id: str
    created_at: datetime
    created_by: str

    # GlucoseLevel fields
    device: str
    serial_number: str
    device_timestamp: str
    recording_type: str
    glucose_value_trend: Optional[str] = None
    glucose_scan: Optional[str] = None
    non_numerical_rapid_acting_insulin: Optional[str] = None
    rapid_acting_insulin: Optional[str] = None
    non_numerical_nutritional_data: Optional[str] = None
    carbohydrates_grams: Optional[str] = None
    carbohydrates_portions: Optional[str] = None
    non_numerical_depot_insulin: Optional[str] = None
    depot_insulin: Optional[str] = None
    notes: Optional[str] = None
    glucose_test_strips: Optional[str] = None
    ketone: Optional[str] = None
    mealtime_insulin: Optional[str] = None
    correction_insulin: Optional[str] = None
    insulin_change_by_user: Optional[str] = None

    def __init__(self, user_id, created_at, created_by, device, serial_number, device_timestamp, 
                 recording_type, glucose_value_trend, glucose_scan, non_numerical_rapid_acting_insulin, 
                 rapid_acting_insulin, non_numerical_nutritional_data, carbohydrates_grams, 
                 carbohydrates_portions, non_numerical_depot_insulin, depot_insulin, notes, 
                 glucose_test_strips, ketone, mealtime_insulin, correction_insulin, insulin_change_by_user):
        self.user_id = user_id
        self.created_at = created_at
        self.created_by = created_by
        self.device = device
        self.serial_number = serial_number
        self.device_timestamp = device_timestamp
        self.recording_type = recording_type
        self.glucose_value_trend = glucose_value_trend
        self.glucose_scan = glucose_scan
        self.non_numerical_rapid_acting_insulin = non_numerical_rapid_acting_insulin
        self.rapid_acting_insulin = rapid_acting_insulin
        self.non_numerical_nutritional_data = non_numerical_nutritional_data
        self.carbohydrates_grams = carbohydrates_grams
        self.carbohydrates_portions = carbohydrates_portions
        self.non_numerical_depot_insulin = non_numerical_depot_insulin
        self.depot_insulin = depot_insulin
        self.notes = notes
        self.glucose_test_strips = glucose_test_strips
        self.ketone = ketone
        self.mealtime_insulin = mealtime_insulin
        self.correction_insulin = correction_insulin
        self.insulin_change_by_user = insulin_change_by_user

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id = data.get('user_id'),
            created_at = datetime.fromisoformat(data.get('created_at')),
            created_by = data.get('created_by'),
            device = data.get('device'),
            serial_number = data.get('serial_number'),
            device_timestamp = datetime.fromisoformat(data.get('device_timestamp')),
            recording_type = data.get('recording_type'),
            glucose_value_trend = data.get('glucose_value_trend'),
            glucose_scan = data.get('glucose_scan'),
            non_numerical_rapid_acting_insulin = data.get('non_numerical_rapid_acting_insulin'),
            rapid_acting_insulin = data.get('rapid_acting_insulin'),
            non_numerical_nutritional_data = data.get('non_numerical_nutritional_data'),
            carbohydrates_grams = data.get('carbohydrates_grams'),
            carbohydrates_portions = data.get('carbohydrates_portions'),
            non_numerical_depot_insulin = data.get('non_numerical_depot_insulin'),
            depot_insulin = data.get('depot_insulin'),
            notes = data.get('notes'),
            glucose_test_strips = data.get('glucose_test_strips'),
            ketone = data.get('ketone'),
            mealtime_insulin = data.get('mealtime_insulin'),
            correction_insulin = data.get('correction_insulin'),
            insulin_change_by_user = data.get('insulin_change_by_user')
        )
