# Generated by Django 4.1.4 on 2023-01-16 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='submitted',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
