# Generated by Django 2.2.16 on 2020-10-08 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perma', '0062_auto_20201007_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalregistrar',
            name='orgs_private_by_default',
            field=models.BooleanField(default=False, help_text='Whether new orgs created for this registrar default to private links.'),
        ),
        migrations.AddField(
            model_name='registrar',
            name='orgs_private_by_default',
            field=models.BooleanField(default=False, help_text='Whether new orgs created for this registrar default to private links.'),
        ),
    ]
