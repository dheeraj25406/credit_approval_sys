from datetime import date
from core.models import Loan

def calculate_credit_score(customer):

    loans=Loan.objects.filter(customer=customer)

    if not loans.exists():
        return 50

    score=0

    total_loans=loans.count()

    on_time=sum(l.emis_paid_on_time for l in loans)
    total_emis=sum(l.tenure for l in loans)

    if total_emis>0:
        score+=40*(on_time/total_emis)

    if total_loans<=2:
        score+=20
    elif total_loans<=5:
        score+=10

    current_year=date.today().year
    recent_loans=loans.filter(start_date__year=current_year).count()

    if recent_loans==0:
        score+=20
    elif recent_loans<=2:
        score+=10

    volume=sum(l.loan_amount for l in loans)

    if volume<customer.approved_limit:
        score+=20
    elif volume<customer.approved_limit*2:
        score+=10

    if volume>customer.approved_limit:
        return 0

    return int(score)