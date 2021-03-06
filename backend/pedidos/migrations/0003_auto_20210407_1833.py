# Generated by Django 3.1.7 on 2021-04-07 18:33

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_pedido_executed'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='pedido',
            constraint=models.CheckConstraint(check=models.Q(end_date__gt=django.db.models.expressions.F('start_date')), name='end_date must be after start_date'),
        ),
    ]
