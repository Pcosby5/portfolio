# Generated by Django 5.0.3 on 2024-03-27 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics/'),
        ),
    ]
