# Generated by Django 3.0.2 on 2020-01-28 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_arvore_submetida'),
    ]

    operations = [
        migrations.AddField(
            model_name='tela',
            name='primeiro',
            field=models.BooleanField(default=False, verbose_name='Primeiro'),
        ),
        migrations.AlterField(
            model_name='raiz',
            name='tela',
            field=models.OneToOneField(help_text='<h1><strong>Ao submeter uma árvore a ser respondinda no site, ela não poderá mais ser editada.</strong></h1>', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Tela'),
        ),
    ]
