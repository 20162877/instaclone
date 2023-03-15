# Generated by Django 4.1.7 on 2023-03-15 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0007_networkedge'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('caption_text', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='users.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('media_file', models.FileField(upload_to='post_media/')),
                ('sequence_index', models.PositiveSmallIntegerField(default=8)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='content.userpost')),
            ],
            options={
                'unique_together': {('sequence_index', 'post')},
            },
        ),
    ]
