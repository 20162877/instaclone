# Generated by Django 4.1.7 on 2023-03-15 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmedia',
            name='media_file',
            field=models.FileField(null=True, upload_to='post_media/'),
        ),
        migrations.AlterField(
            model_name='postmedia',
            name='sequence_index',
            field=models.PositiveSmallIntegerField(default=8, null=True),
        ),
    ]
