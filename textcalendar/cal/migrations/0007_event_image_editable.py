# Generated by Django 4.2.7 on 2024-06-01 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0006_alter_event_bottom_clothes_alter_event_outer_clothes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image_editable',
            field=models.BooleanField(default=True),
        ),
    ]
