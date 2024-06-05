# Generated by Django 4.2.7 on 2024-06-01 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0002_alter_event_description_alter_event_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
