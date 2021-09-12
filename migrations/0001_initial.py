# Generated by Django 3.2.7 on 2021-09-12 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=150)),
                ('berid', models.CharField(blank=True, max_length=3)),
                ('street', models.CharField(blank=True, max_length=100)),
                ('zip', models.CharField(blank=True, max_length=5)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('geo', models.CharField(blank=True, max_length=100)),
                ('publictransport', models.CharField(blank=True, max_length=100)),
                ('contactperson', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(blank=True, max_length=100)),
                ('mail', models.CharField(blank=True, max_length=100)),
                ('commentintern', models.TextField(blank=True, max_length=800)),
                ('commentextern', models.TextField(blank=True, max_length=800)),
                ('interview', models.TextField(blank=True, max_length=800)),
                ('biost', models.BooleanField(default=False)),
                ('care', models.BooleanField(default=False)),
                ('efz', models.BooleanField(default=False)),
                ('driverlicence', models.BooleanField(default=False)),
                ('least18', models.BooleanField(default=False)),
                ('allcourse', models.BooleanField(default=False)),
                ('todo', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Metacontent',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('path', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('mapbox', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('contactperson', models.CharField(blank=True, max_length=100)),
                ('street', models.CharField(blank=True, max_length=100)),
                ('zip', models.CharField(blank=True, max_length=5)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(blank=True, max_length=100)),
                ('mail', models.EmailField(blank=True, max_length=254)),
                ('homepage', models.URLField(blank=True, max_length=300)),
                ('comment', models.TextField(blank=True, max_length=800)),
                ('schule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='frieda.school')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InternshipAssignment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ablock', models.CharField(blank=True, max_length=100)),
                ('bblock', models.CharField(blank=True, max_length=100)),
                ('student_a_1', models.CharField(blank=True, max_length=100)),
                ('student_b_1', models.CharField(blank=True, max_length=100)),
                ('student_a_2', models.CharField(blank=True, max_length=100)),
                ('student_b_2', models.CharField(blank=True, max_length=100)),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='frieda.internship')),
                ('schoolyear', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='frieda.schoolyear')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='internship',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='frieda.organisation'),
        ),
    ]
