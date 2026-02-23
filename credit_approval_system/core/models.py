from django.db import models

class Customer(models.Model):
    customer_id=models.IntegerField(unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    age=models.IntegerField()
    phone_number=models.BigIntegerField()
    monthly_income=models.FloatField()
    approved_limit=models.FloatField()
    current_debt=models.FloatField(default=0)

    def __str__(self):
        return f"{self.customer_id}-{self.first_name}"

class Loan(models.Model):
    loan_id=models.IntegerField(unique=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    loan_amount=models.FloatField()
    tenure=models.IntegerField()
    interest_rate=models.FloatField()
    monthly_installment=models.FloatField()
    emis_paid_on_time=models.IntegerField()
    start_date=models.DateField()
    end_date=models.DateField()

    def __str__(self):
        return str(self.loan_id)