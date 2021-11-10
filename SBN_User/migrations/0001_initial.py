# Generated by Django 3.2.9 on 2021-11-10 08:34

import SBN_User.models
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserPlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(help_text='Following format: char(1 -> 8).', max_length=8, verbose_name='user_category.')),
            ],
            options={
                'verbose_name': 'user_platform.',
                'verbose_name_plural': 'user_platforms.',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('uid', models.CharField(help_text='Following format: char(1 -> 28).', max_length=28, primary_key=True, serialize=False, unique=True, verbose_name='user_uid.')),
                ('username', models.CharField(help_text='Following format: char(1 -> 20).', max_length=20, verbose_name='user_username.')),
                ('email', models.EmailField(help_text='Following format: char(1 -> 40).', max_length=40, unique=True, verbose_name='user_email.')),
                ('full_name', models.CharField(help_text='Following format: char(1 -> 40).', max_length=40, verbose_name='full_name.')),
                ('first_dest', models.CharField(help_text='Following format: char(1 -> 40).', max_length=40, verbose_name='first_destination.')),
                ('second_dest', models.CharField(help_text='Following format: char(1 -> 40).', max_length=40, verbose_name='second_destination.')),
                ('third_dest', models.CharField(help_text='Following format: char(1 -> 40).', max_length=40, verbose_name='third_destination.')),
                ('detail_adr', models.TextField(help_text='Following format: char(1 -> 40).', max_length=200, verbose_name='detail_address.')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('avatar', models.ImageField(default='images/default/avatar.png', help_text='Your avatar image link.', upload_to=SBN_User.models.ImageAvatarPath('images/'), verbose_name='avatar_image.')),
                ('avatar_alt', models.CharField(help_text='Following format: char(1 -> 200).', max_length=200, verbose_name='avatar_alt_text.')),
                ('background', models.ImageField(default='images/default/background.png', help_text='Your background image link.', upload_to=SBN_User.models.ImageBackgroundPath('images/'), verbose_name='background_image.')),
                ('background_alt', models.CharField(help_text='Following format: char(1 -> 200).', max_length=200, verbose_name='background_alt_text.')),
                ('platform', models.ForeignKey(help_text='Each User Tables (UserInfo and UserAuth) have only 1 platform.', on_delete=django.db.models.deletion.CASCADE, to='SBN_User.userplatform', verbose_name='user_platform.')),
            ],
            options={
                'verbose_name': 'user_uid.',
                'verbose_name_plural': 'user_uids.',
            },
        ),
        migrations.CreateModel(
            name='UserAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='Following format: char(1 -> 20).', max_length=20, verbose_name='user_username.')),
                ('email', models.EmailField(help_text='Following format: char(1 -> 40).', max_length=40, unique=True, verbose_name='user_email.')),
                ('password', models.CharField(help_text='Hashed password using SHA-256. char(64).', max_length=64, verbose_name='user_password.')),
                ('is_verified', models.BooleanField(default=False, help_text='Account has been verified?', verbose_name='user_verified?')),
                ('is_updated', models.BooleanField(default=False, help_text='Account has been updated?', verbose_name='user_updated?')),
                ('uid', models.ForeignKey(help_text='Following format: char(1 -> 28).', on_delete=django.db.models.deletion.CASCADE, to='SBN_User.userinfo', verbose_name='user_uid.')),
            ],
            options={
                'verbose_name': 'user_auth.',
                'verbose_name_plural': 'user_auths.',
            },
        ),
    ]
