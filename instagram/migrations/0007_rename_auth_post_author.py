# Generated by Django 4.0.3 on 2022-03-13 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0006_tag_post_tag_set'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='auth',
            new_name='author',
        ),
    ]
