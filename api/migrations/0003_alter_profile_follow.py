# Generated by Django 5.0.6 on 2024-09-02 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_profile_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='follow',
            field=models.ManyToManyField(blank=True, null=True, related_name='followers_followings', to='api.profile'),
        ),
    ]
