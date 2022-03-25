# Generated by Django 4.0.3 on 2022-03-25 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_template_options_hotel_region_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='date_from',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='date_to',
        ),
        migrations.AddField(
            model_name='booking',
            name='days',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
