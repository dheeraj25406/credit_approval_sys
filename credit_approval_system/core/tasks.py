import pandas as pd
import logging
from django.conf import settings
from django.db import transaction
from celery import shared_task
from .models import Customer,Loan

logger=logging.getLogger(__name__)


@shared_task(bind=True,autoretry_for=(IOError,),retry_backoff=True,retry_kwargs={"max_retries":3})
def load_initial_data(self):
    logger.info("Starting Excel ingestion task")

    # prevent duplicate ingestion
    if Customer.objects.exists() and Loan.objects.exists():
        logger.info("Data already loaded — skipping")
        return

    customer_file=f"{settings.BASE_DIR}/customer_data.xlsx"
    loan_file=f"{settings.BASE_DIR}/loan_data.xlsx"

    cust_df=pd.read_excel(customer_file)
    loan_df=pd.read_excel(loan_file)

    # remove hidden spaces in column names
    cust_df.columns=cust_df.columns.str.strip()
    loan_df.columns=loan_df.columns.str.strip()

    with transaction.atomic():

        existing_customers={
            c.customer_id:c
            for c in Customer.objects.all()
        }

        new_customers=[]
        update_customers=[]

        for _,r in cust_df.iterrows():
            cid=int(r["Customer ID"])

            obj=dict(
                first_name=str(r["First Name"]).strip(),
                last_name=str(r["Last Name"]).strip(),
                age=int(r["Age"]),
                phone_number=int(r["Phone Number"]),
                monthly_income=float(r["Monthly Salary"]),
                approved_limit=float(r["Approved Limit"])
            )

            if cid in existing_customers:
                cust_obj=existing_customers[cid]
                for k,v in obj.items():
                    setattr(cust_obj,k,v)
                update_customers.append(cust_obj)
            else:
                new_customers.append(Customer(customer_id=cid,**obj))

        if new_customers:
            Customer.objects.bulk_create(new_customers)

        if update_customers:
            Customer.objects.bulk_update(
                update_customers,
                ["first_name","last_name","age","phone_number","monthly_income","approved_limit"]
            )

        logger.info(f"Customers inserted={len(new_customers)} updated={len(update_customers)}")

        # refresh map after inserts
        customer_map={
            c.customer_id:c
            for c in Customer.objects.all()
        }

        existing_loans={
            l.loan_id:l
            for l in Loan.objects.all()
        }

        new_loans=[]
        update_loans=[]

        for _,r in loan_df.iterrows():
            lid=int(r["Loan ID"])

            obj=dict(
                customer=customer_map.get(int(r["Customer ID"])),
                loan_amount=float(r["Loan Amount"]),
                tenure=int(r["Tenure"]),
                interest_rate=float(r["Interest Rate"]),
                monthly_installment=float(r["Monthly payment"]),
                emis_paid_on_time=int(r["EMIs paid on Time"]),
                start_date=pd.to_datetime(r["Date of Approval"]).date(),
                end_date=pd.to_datetime(r["End Date"]).date()
            )

            if lid in existing_loans:
                loan_obj=existing_loans[lid]
                for k,v in obj.items():
                    setattr(loan_obj,k,v)
                update_loans.append(loan_obj)
            else:
                new_loans.append(Loan(loan_id=lid,**obj))

        if new_loans:
            Loan.objects.bulk_create(new_loans,ignore_conflicts=True)

        if update_loans:
            Loan.objects.bulk_update(
                update_loans,
                ["customer","loan_amount","tenure","interest_rate","monthly_installment","emis_paid_on_time","start_date","end_date"]
            )

        logger.info(f"Loans inserted={len(new_loans)} updated={len(update_loans)}")

    logger.info("Excel ingestion completed successfully")