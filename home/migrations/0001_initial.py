# Generated by Django 2.1.1 on 2018-10-30 01:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('C_Name', models.CharField(max_length=50, null=True)),
                ('C_Type', models.CharField(max_length=50, null=True)),
                ('current_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('F_Name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Location', models.CharField(max_length=100)),
                ('Description', models.TextField()),
                ('Facility_Hours', models.TextField(blank=True, null=True)),
                ('Facility_Phone', models.CharField(blank=True, max_length=15, null=True)),
                ('Parking_Hours', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Our_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reserved_Time_Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Court')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Facility')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Our_User')),
            ],
        ),
        migrations.CreateModel(
            name='Time_Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Slot', models.DateTimeField()),
                ('available', models.BooleanField(default=True)),
                ('signup_count', models.IntegerField(default=0)),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Court')),
            ],
        ),
        migrations.AddField(
            model_name='court',
            name='facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Facility'),
        ),
    ]