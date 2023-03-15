# Generated by Django 4.1.7 on 2023-03-15 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_alter_postmedia_media_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmedia',
            name='media_file',
            field=models.FileField(upload_to='post_media/'),
        ),
        migrations.AlterField(
            model_name='postmedia',
            name='sequence_index',
            field=models.PositiveSmallIntegerField(default=8),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='caption_text',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='location',
            field=models.CharField(max_length=200, null=True),
        ),
    ]