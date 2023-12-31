# Generated by Django 3.2.19 on 2023-06-13 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_list', '0004_alter_mail_mailing_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='status',
            field=models.CharField(choices=[('success', 'Success'), ('failed', 'Failed'), ('pending', 'Pending'), ('canceled', 'Canceled')], default='Pending', max_length=10),
        ),
    ]
