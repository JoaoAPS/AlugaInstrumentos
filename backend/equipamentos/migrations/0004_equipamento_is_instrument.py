# Generated by Django 3.2 on 2021-04-14 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0003_auto_20210406_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipamento',
            name='is_instrument',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
