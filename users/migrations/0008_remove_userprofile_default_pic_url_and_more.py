# Generated by Django 4.1.7 on 2023-03-15 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_networkedge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='default_pic_url',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_pic_url',
            field=models.ImageField(blank=True, upload_to='profile_pic/'),
        ),
    ]
