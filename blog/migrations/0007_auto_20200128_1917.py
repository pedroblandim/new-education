# Generated by Django 3.0.2 on 2020-01-28 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_arvore_prim_tela'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arvore',
            name='prim_tela',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prim_tela', to='blog.Tela'),
        ),
    ]
