# Generated by Django 3.0.2 on 2020-01-28 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200128_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tela',
            name='primeiro',
        ),
    ]