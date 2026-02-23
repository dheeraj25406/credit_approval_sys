from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import Customer,Loan
from .serializers import *
from .services.emi import calculate_emi
from .services.eligibility import credit_score,interest_correction,can_approve
from .utils import round_to_lakh
import random
from datetime import date
from dateutil.relativedelta import relativedelta


@api_view(['GET'])
def home(request):
    return Response({"message":"Credit Approval API running"})


# register customer
@api_view(['POST'])
def register(request):
    s=RegisterSerializer(data=request.data)
    if not s.is_valid(): return Response(s.errors,400)

    d=s.validated_data

    cid=random.randint(1000,9999)
    while Customer.objects.filter(customer_id=cid).exists():
        cid=random.randint(1000,9999)

    limit=round_to_lakh(36*d['monthly_income'])

    c=Customer.objects.create(
        customer_id=cid,
        approved_limit=limit,
        current_debt=0,
        **d
    )

    return Response({
        "customer_id":c.customer_id,
        "name":c.first_name+" "+c.last_name,
        "age":c.age,
        "monthly_income":c.monthly_income,
        "approved_limit":c.approved_limit,
        "phone_number":c.phone_number
    })


# checking eligibility
@api_view(['POST'])
def check_eligibility(request):
    s=EligibilitySerializer(data=request.data)   # ✅ FIXED SERIALIZER
    if not s.is_valid(): return Response(s.errors,400)

    d=s.validated_data

    try:
        c=Customer.objects.get(customer_id=d['customer_id'])
    except Customer.DoesNotExist:
        return Response({"error":"Customer not found"},404)

    score=credit_score(c)

    emi=calculate_emi(
        d['loan_amount'],
        d['interest_rate'],
        d['tenure']
    )

    corrected=interest_correction(score,d['interest_rate'])

    approved=can_approve(
        c,
        score,
        corrected if corrected else d['interest_rate'],
        emi
    )

    return Response({
        "customer_id":c.customer_id,
        "approval":approved,
        "interest_rate":d['interest_rate'],
        "corrected_interest_rate":corrected if corrected else d['interest_rate'],
        "credit_score":score,
        "tenure":d['tenure'],
        "monthly_installment":round(emi,2)
    })


# create loan
@api_view(['POST'])
def create_loan(request):
    s=CreateLoanSerializer(data=request.data)
    if not s.is_valid(): return Response(s.errors,400)

    d=s.validated_data

    try:
        c=Customer.objects.get(customer_id=d['customer_id'])
    except Customer.DoesNotExist:
        return Response({"error":"Customer not found"},404)

    score=credit_score(c)

    corrected=interest_correction(score,d['interest_rate'])

    rate=corrected if corrected else d['interest_rate']

    emi=calculate_emi(
        d['loan_amount'],
        rate,
        d['tenure']
    )

    approved=can_approve(c,score,rate,emi)

    if not approved:
        return Response({
            "loan_id":None,
            "customer_id":c.customer_id,
            "loan_approved":False,
            "message":"Loan not approved",
            "monthly_installment":round(emi,2)
        })

    with transaction.atomic():

        lid=random.randint(10000,99999)
        while Loan.objects.filter(loan_id=lid).exists():
            lid=random.randint(10000,99999)

        start=date.today()
        end=start+relativedelta(months=d['tenure'])

        Loan.objects.create(
            loan_id=lid,
            customer=c,
            loan_amount=d['loan_amount'],
            tenure=d['tenure'],
            interest_rate=rate,
            monthly_installment=emi,
            emis_paid_on_time=0,
            start_date=start,
            end_date=end
        )

        c.current_debt+=d['loan_amount']
        c.save()

    return Response({
        "loan_id":lid,
        "customer_id":c.customer_id,
        "loan_approved":True,
        "message":"Approved",
        "monthly_installment":round(emi,2)
    })


# view single loan
@api_view(['GET'])
def view_loan(request,loan_id):

    try:
        l=Loan.objects.get(loan_id=loan_id)
    except Loan.DoesNotExist:
        return Response({"error":"Loan not found"},404)

    c=l.customer

    return Response({
        "loan_id":l.loan_id,
        "customer":{
            "id":c.customer_id,
            "first_name":c.first_name,
            "last_name":c.last_name,
            "phone_number":c.phone_number,
            "age":c.age
        },
        "loan_amount":l.loan_amount,
        "interest_rate":l.interest_rate,
        "monthly_installment":round(l.monthly_installment,2),
        "tenure":l.tenure
    })


# view all loans
@api_view(['GET'])
def view_loans(request,customer_id):

    loans=Loan.objects.filter(customer__customer_id=customer_id)

    out=[]
    for l in loans:
        out.append({
            "loan_id":l.loan_id,
            "loan_amount":l.loan_amount,
            "interest_rate":l.interest_rate,
            "monthly_installment":round(l.monthly_installment,2),
            "repayments_left":l.tenure-l.emis_paid_on_time
        })

    return Response(out)