# Generated by Django 2.0 on 2017-12-26 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20171226_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(1, 'Aberto'), (2, 'Cancelado'), (3, 'Aguardando pagamento'), (4, 'Pagamento recusado'), (5, 'Pago'), (6, 'Despachado'), (7, 'Entregue'), (8, 'Estornado'), (9, 'Devolvido')])),
                ('coupon', models.CharField(max_length=30)),
                ('date_expired', models.DateTimeField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('address_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Address')),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Person')),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Product')),
            ],
            options={
                'db_table': 'order_product',
            },
        ),
    ]