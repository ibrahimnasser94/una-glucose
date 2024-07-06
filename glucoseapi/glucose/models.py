from django.db import models

class GlucoseLevelMetadata(models.Model):
    """
    Represents metadata for a glucose level entry.

    Attributes:
        user_id (str): The ID of the user associated with the glucose level.
        created_at (datetime): The date and time when the glucose level was created.
        created_by (str): The name of the user who created the glucose level entry.
    """
    user_id =  models.CharField(max_length=200, verbose_name="User ID")
    created_at = models.DateTimeField("Erstellt am")
    created_by = models.CharField(max_length=200, verbose_name="Erstellt von")

class GlucoseLevel(models.Model):
    """
    Represents a glucose level measurement.

    Attributes:
        metadata (ForeignKey): The metadata associated with the glucose level.
        device (CharField): The device used for measurement.
        serial_number (CharField): The serial number of the device.
        device_timestamp (CharField): The timestamp recorded by the device.
        recording_type (CharField): The type of recording.
        glucose_value_trend (CharField): The trend of glucose value in mg/dL (milligrams per deciliter).
        glucose_scan (CharField): The glucose scan in mg/dL.
        non_numerical_rapid_acting_insulin (CharField): Non-numerical rapid-acting insulin.
        rapid_acting_insulin (CharField): Rapid-acting insulin in units.
        non_numerical_nutritional_data (CharField): Non-numerical nutritional data.
        carbohydrates_grams (CharField): Carbohydrates in grams.
        carbohydrates_portions (CharField): Carbohydrates in portions.
        non_numerical_depot_insulin (CharField): Non-numerical depot insulin.
        depot_insulin (CharField): Depot insulin in units.
        notes (CharField): Additional notes.
        glucose_test_strips (CharField): Glucose test strips in mg/dL.
        ketone (CharField): Ketone measurement in mmol/L (millimoles per liter).
        mealtime_insulin (CharField): Mealtime insulin in units.
        correction_insulin (CharField): Correction insulin in units.
        insulin_change_by_user (CharField): Insulin change made by the user in units.
    """

    metadata = models.ForeignKey(GlucoseLevelMetadata, on_delete=models.CASCADE)
    device = models.CharField(max_length=200, verbose_name="Gerät")
    serial_number = models.CharField(max_length=200, verbose_name="Seriennummer")
    device_timestamp = models.CharField(max_length=200, verbose_name="Gerätezeitstempel")
    recording_type = models.CharField(max_length=200, verbose_name="Aufzeichnungstyp")
    glucose_value_trend = models.CharField(max_length=200, verbose_name="Glukosewert-Verlauf mg/dL", null=True)
    glucose_scan = models.CharField(max_length=200, verbose_name="Glukose-Scan mg/dL", null=True)
    non_numerical_rapid_acting_insulin = models.CharField(max_length=200, verbose_name="Nicht numerisches schnellwirkendes Insulin", null=True)
    rapid_acting_insulin = models.CharField(max_length=200, verbose_name="Schnellwirkendes Insulin (Einheiten)", null=True)
    non_numerical_nutritional_data = models.CharField(max_length=200, verbose_name="Nicht numerische Nahrungsdaten", null=True)
    carbohydrates_grams = models.CharField(max_length=200, verbose_name="Kohlenhydrate (Gramm)", null=True)
    carbohydrates_portions = models.CharField(max_length=200, verbose_name="Kohlenhydrate (Portionen)", null=True)
    non_numerical_depot_insulin = models.CharField(max_length=200, verbose_name="Nicht numerisches Depotinsulin", null=True)
    depot_insulin = models.CharField(max_length=200, verbose_name="Depotinsulin (Einheiten)", null=True)
    notes = models.CharField(max_length=200, verbose_name="Notizen", null=True)
    glucose_test_strips = models.CharField(max_length=200, verbose_name="Glukose-Teststreifen mg/dL", null=True)
    ketone = models.CharField(max_length=200, verbose_name="Keton mmol/L", null=True)
    mealtime_insulin = models.CharField(max_length=200, verbose_name="Mahlzeiteninsulin (Einheiten)", null=True)
    correction_insulin = models.CharField(max_length=200, verbose_name="Korrekturinsulin (Einheiten)", null=True)
    insulin_change_by_user = models.CharField(max_length=200, verbose_name="Insulin-Änderung durch Anwender (Einheiten)", null=True)





