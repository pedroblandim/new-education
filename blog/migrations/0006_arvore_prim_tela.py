# Generated by Django 3.0.2 on 2020-01-28 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_remove_tela_primeiro'),
    ]

    operations = [
        migrations.AddField(
            model_name='arvore',
            name='prim_tela',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]