# Generated by Django 4.1.4 on 2022-12-21 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_financials_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='financials',
            options={'ordering': ['-reporting_period']},
        ),
    ]
