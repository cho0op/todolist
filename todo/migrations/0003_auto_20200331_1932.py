# Generated by Django 3.0.4 on 2020-03-31 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20200331_1837'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='compliting_date',
            new_name='completing_date',
        ),
    ]
