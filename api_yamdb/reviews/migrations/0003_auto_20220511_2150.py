# Generated by Django 2.2.16 on 2022-05-11 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220511_1520'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='created',
            new_name='pub_date',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='review',
            new_name='review_id',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='titles',
            new_name='title_id',
        ),
    ]
