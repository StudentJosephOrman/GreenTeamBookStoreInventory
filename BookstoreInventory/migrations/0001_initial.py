# Generated by Django 4.2.7 on 2023-12-05 05:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('middle_name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=120)),
                ('genre', models.CharField(max_length=80)),
                ('summary', models.CharField(max_length=120)),
                ('quantity', models.IntegerField()),
                ('cost', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('authors', models.ManyToManyField(db_column='author_ids', to='BookstoreInventory.author')),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80, unique=True)),
                ('location', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=80)),
                ('user_type', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='user_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('middle_name', models.CharField(max_length=80)),
                ('date', models.DateField()),
                ('cost', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('book_isbn', models.ForeignKey(db_column='isbn', on_delete=django.db.models.deletion.CASCADE, to='BookstoreInventory.book')),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('company', models.CharField(max_length=120)),
                ('expected_date', models.DateField()),
                ('cost', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('delivered', models.BooleanField()),
                ('transaction', models.ForeignKey(db_column='transaction_id', on_delete=django.db.models.deletion.CASCADE, to='BookstoreInventory.transaction')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(db_column='publisher_id', on_delete=django.db.models.deletion.CASCADE, to='BookstoreInventory.publisher'),
        ),
    ]