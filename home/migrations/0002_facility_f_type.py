# Generated by Django 2.1.1 on 2018-11-01 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='F_Type',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
