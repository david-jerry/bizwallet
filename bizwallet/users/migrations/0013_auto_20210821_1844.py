# Generated by Django 3.1.12 on 2021-08-21 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210821_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginhistory',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='User IP'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='features',
            field=models.ManyToManyField(to='users.MembershipFeature'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='membership_type',
            field=models.CharField(choices=[('Free', 'Free'), ('Premium', 'Premium'), ('Platinum', 'Platinum'), ('Gold', 'Gold'), ('VIP', 'VIP'), ('VVIP', 'VVIP')], default='Premium', max_length=30),
        ),
    ]
