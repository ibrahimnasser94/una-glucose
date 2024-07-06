import datetime
from typing import Dict
from django.db import migrations
import os
import csv
from glucose.models import GlucoseLevel, GlucoseLevelMetadata
from glucose.utils import get_field_from_verbose


DATA_FOLDER = "/Users/ibrahimnasser/Desktop/Personals/Professional/una-glucose/glucoseapi/glucose/data"
DATE_FORMAT = "%d-%m-%Y %H:%M UTC"


def populate_data(apps, schema_editor):
    """
    Populates the database with data from CSV files in the specified directory.

    Args:
        apps: A reference to the application registry.
        schema_editor: The schema editor used for database operations.

    Returns:
        None
    """
    
    # Encodes directory
    directory = os.fsencode(DATA_FOLDER)

    # Iterate over files in the directory
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        
        # Check if the file is a CSV file
        if filename.endswith(".csv"):
            file_path = os.path.join(DATA_FOLDER, filename)
            
            # Open the CSV file
            with open(file_path, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                
                # Read the metadata row
                metadata_row = next(spamreader)  
                
                # Create a GlucoseLevelMetadata object with the metadata values
                metadata_object = GlucoseLevelMetadata.objects.create(**{
                    "user_id": filename.removesuffix(".csv"),
                    "created_at": datetime.datetime.strptime(metadata_row[2], DATE_FORMAT).date(),
                    "created_by": metadata_row[4]
                })
                
                # Read the header row
                header_row = next(spamreader)
                
                # If the header row is empty, read the next row
                if not any(header_row):
                    header_row = next(spamreader)
                
                # Get the field names from the header row
                field_names = [get_field_from_verbose(GlucoseLevel._meta, key) for key in header_row]
                
                # Read the data rows
                data = [row for row in spamreader]
                
                # Create a dictionary for each data row with field names as keys
                data = [dict(zip(field_names, row)) for row in data]
                
                # Set the metadata object for each data row and create a GlucoseLevel object
                for obj in data:
                    obj['metadata'] = metadata_object
                    GlucoseLevel.objects.create(**obj)
            
            continue
        else:
            continue

class Migration(migrations.Migration):

    dependencies = [
        ('glucose', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_data, lambda apps, schema_editor: None),
    ]
