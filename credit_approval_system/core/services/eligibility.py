from datetime import date
from core.models import Loan

def credit_score(customer):
    loans=Loan.objects.filter(customer=customer)
    if not loans.exists():
        return 50

    paid=sum(l.emis_paid_on_time for l in loans)
    total=sum(l.tenure for l in loans)
    ratio=paid/total if total else 0

    count=loans.count()
    volume=sum(l.loan_amount for l in loans)
    year_loans=loans.filter(start_date__year=date.today().year).count()

    score=0
    score+=ratio*40
    score+=max(0,20-count)
    score+=max(0,20-year_loans)
    score+=max(0,20-(volume/1000000))

    if customer.current_debt>customer.approved_limit:
        return 0

    return int(score)


def interest_correction(score,rate):
    if score>50:
        return rate
    elif 50>=score>30:
        return max(rate,12)
    elif 30>=score>10:
        return max(rate,16)
    else:
        return None


def can_approve(customer,score,rate,emi):

    if customer.current_debt>customer.approved_limit:
        return False

    if emi>customer.monthly_income*0.5:
        return False

    if score<=10:
        return False

    if score>50:
        return True

    elif 50>=score>30:
        return True

    elif 30>=score>10:
        return True

    return False