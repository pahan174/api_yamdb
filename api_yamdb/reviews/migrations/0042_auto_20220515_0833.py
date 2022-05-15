# Generated by Django 2.2.16 on 2022-05-15 03:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0041_auto_20220515_0821'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_author_title',
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('author', 'title')},
        ),
    ]
