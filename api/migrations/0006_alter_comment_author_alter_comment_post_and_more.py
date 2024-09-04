# Generated by Django 4.2.14 on 2024-09-02 23:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='api.post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='parent_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='api.tag'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='follow',
            field=models.ManyToManyField(blank=True, related_name='followers_followings', to='api.profile'),
        ),
    ]