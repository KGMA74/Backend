# Generated by Django 5.0.6 on 2024-07-02 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(fields=('owner', 'post'), name='unique_user_post_vote'),
        ),
    ]
