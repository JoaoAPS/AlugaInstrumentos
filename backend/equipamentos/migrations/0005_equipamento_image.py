# Generated by Django 3.2 on 2021-04-14 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0004_equipamento_is_instrument'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipamento',
            name='image',
            field=models.ImageField(default=None, upload_to='equipaments'),
            preserve_default=False,
        ),
    ]
