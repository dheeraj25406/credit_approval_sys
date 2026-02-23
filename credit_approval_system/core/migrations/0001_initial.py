from django.db import migrations,models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial=True

    dependencies=[]

    operations=[
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id',models.BigAutoField(primary_key=True,serialize=False)),
                ('customer_id',models.IntegerField(unique=True)),
                ('first_name',models.CharField(max_length=100)),
                ('last_name',models.CharField(max_length=100)),
                ('age',models.IntegerField()),
                ('phone_number',models.BigIntegerField()),
                ('monthly_salary',models.FloatField()),
                ('approved_limit',models.FloatField()),
                ('current_debt',models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id',models.BigAutoField(primary_key=True,serialize=False)),
                ('loan_id',models.IntegerField(unique=True)),
                ('loan_amount',models.FloatField()),
                ('tenure',models.IntegerField()),
                ('interest_rate',models.FloatField()),
                ('monthly_installment',models.FloatField()),
                ('emis_paid_on_time',models.IntegerField()),
                ('start_date',models.DateField()),
                ('end_date',models.DateField()),
                ('customer',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to='core.customer')),
            ],
        ),
    ]