# Generated by Django 4.2.16 on 2024-09-28 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_estoque'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forma', models.IntegerField(choices=[(1, 'Dinheiro'), (2, 'Cartão'), (3, 'Pix'), (4, 'Outra')])),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_pgto', models.DateTimeField(auto_now_add=True)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.pedido')),
            ],
        ),
    ]
