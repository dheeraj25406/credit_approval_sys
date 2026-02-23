from rest_framework import serializers
from .models import Customer

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model=Customer
        fields=[
            "customer_id",
            "first_name",
            "last_name",
            "age",
            "monthly_income",
            "approved_limit",
            "phone_number"
        ]
        read_only_fields=["customer_id","approved_limit"]

    def create(self,data):
        income=data["monthly_income"]
        data["approved_limit"]=round((36*income)/100000)*100000
        return Customer.objects.create(**data)
    
from rest_framework import serializers

class EligibilitySerializer(serializers.Serializer):
    customer_id=serializers.IntegerField()
    loan_amount=serializers.FloatField()
    interest_rate=serializers.FloatField()
    tenure=serializers.IntegerField()

from rest_framework import serializers

class CreateLoanSerializer(serializers.Serializer):
    customer_id=serializers.IntegerField()
    loan_amount=serializers.FloatField()
    interest_rate=serializers.FloatField()
    tenure=serializers.IntegerField()