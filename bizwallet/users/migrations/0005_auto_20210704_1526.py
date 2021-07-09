# Generated by Django 3.1.12 on 2021-07-04 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210704_0408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='accept_terms',
            field=models.BooleanField(default=False, verbose_name='Accept our terms'),
        ),
        migrations.AlterField(
            model_name='user',
            name='has_paid',
            field=models.BooleanField(default=False, verbose_name='User has Paid'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_field_worker',
            field=models.BooleanField(default=False, verbose_name='Are you a field worker'),
        ),
    ]
