# Generated by Django 2.0.2 on 2018-07-06 05:32

from django.db import migrations

import json

# Reads records from departures.json and creates and inserts 
# corresponding records into Django database

def import_departures_csv(apps, schema_editor):

    with open('departures.json', 'r') as f:
        departures = json.load(f)

    Departure = apps.get_model('departures', 'Departure')
    
    for item in departures:
        departure_record = Departure(
                                name=item['name'], 
                                start_date=item['start_date'], 
                                finish_date=item['finish_date'],
                                category=item['category'])
        departure_record.save()


class Migration(migrations.Migration):

    dependencies = [
        ('departures', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_departures_csv)
    ]
