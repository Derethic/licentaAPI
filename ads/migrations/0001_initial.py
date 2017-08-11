# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-24 20:00
from __future__ import unicode_literals

import ads.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('location', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('user_created_at', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField(max_length=15)),
                ('currency', models.CharField(max_length=10)),
                ('condition', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=3000)),
                ('view_count', models.IntegerField(blank=True, default=0, editable=False)),
                ('ad_created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture1', models.ImageField(blank=True, help_text='Ad Picture', null=True, upload_to=ads.models.UploadToPathAndRename('pictures'), verbose_name='Ad Picture')),
                ('picture2', models.ImageField(blank=True, help_text='Ad Picture', null=True, upload_to=ads.models.UploadToPathAndRename('pictures'), verbose_name='Ad Picture')),
                ('picture3', models.ImageField(blank=True, help_text='Ad Picture', null=True, upload_to=ads.models.UploadToPathAndRename('pictures'), verbose_name='Ad Picture')),
                ('picture4', models.ImageField(blank=True, help_text='Ad Picture', null=True, upload_to=ads.models.UploadToPathAndRename('pictures'), verbose_name='Ad Picture')),
            ],
        ),
        migrations.CreateModel(
            name='MCateg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=3000)),
                ('read_time', models.DateTimeField(blank=True, null=True)),
                ('message_created_at', models.DateTimeField(auto_now_add=True)),
                ('message_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_message_receivers', to=settings.AUTH_USER_MODEL)),
                ('message_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads_message_senders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='mcateg',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.Subcategory'),
        ),
        migrations.AddField(
            model_name='ad',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.Gallery'),
        ),
        migrations.AddField(
            model_name='ad',
            name='mapcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.MCateg'),
        ),
        migrations.AddField(
            model_name='ad',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]