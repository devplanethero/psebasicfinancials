# Generated by Django 4.1.4 on 2022-12-21 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_financials_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='financials',
            options={'ordering': ['-year']},
        ),
    ]
