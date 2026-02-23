# Credit Approval System
A backend system for managing customers, evaluating loan eligibility, and approving loans based on financial and credit behavior. Built using Django, Django REST Framework, PostgreSQL, Docker, and Celery for asynchronous processing.

# Features
- Register customers
- Calculate approved credit limit automatically
- Check loan eligibility based on rules
- Create loans with EMI calculation
- View loan details
- View all loans of a customer
- Bulk import Excel data asynchronously
- Fully Dockerized environment

# Credit Evaluation Logic

Eligibility is calculated using:
- Past repayment performance
- Number of loans taken
- Total loan volume
- Loans taken in current year
- Current debt vs approved limit
- EMI must be ≤ 50% of monthly income

Score Rules:
- Score > 50 → Approved
- Score 30–50 → Approved only if interest > 12%
- Score 10–30 → Approved only if interest > 16%
- Score < 10 → Rejected

# Tech Stack

Backend: Django + DRF
Database: PostgreSQL
Queue: Celery + Redis
Containers: Docker
Data Processing: Pandas

# Project Structure

- credit_approval_system/
  - credit_system/
    - __init__.py
    - settings.py
    - urls.py
    - asgi.py
    - wsgi.py
    - celery.py
  - core/
    - __init__.py
    - admin.py
    - apps.py
    - models.py
    - views.py
    - serializers.py
    - tasks.py
    - migrations/
    - services/
      - __init__.py
      - eligibility.py
      - emi.py
    - utils.py
  - customer_data.xlsx
  - loan_data.xlsx
  - manage.py
  - Dockerfile
  - docker-compose.yml
  - requirements.txt
  - README.md

# Setup Instructions

Clone repo
```bash
git clone https://github.com/dheeraj25406/credit_approval_system
cd credit_approval_system
```

Start containers

```bash
docker compose up --build
```

Run migrations
```bash
docker compose exec web python manage.py migrate
```

Load initial Excel data

```bash
docker compose exec web python manage.py shell
```

then run

```bash
from core.tasks import load_initial_data
load_initial_data.delay()
```

## API Endpoints

### Register Customer

**POST** `/register`

**Request JSON**

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "age": 25,
  "monthly_income": 50000,
  "phone_number": 9999999999
}
```

---

### Check Eligibility

**POST** `/check-eligibility`

```json
{
  "customer_id": 1234,
  "loan_amount": 200000,
  "interest_rate": 12,
  "tenure": 24
}
```

---

### Create Loan

**POST** `/create-loan`

---

### View Loan

**GET** `/view-loan/<loan_id>`

---

### View Customer Loans

**GET** `/view-loans/<customer_id>`

---

## EMI Formula

```
EMI = (P × r × (1+r)^n) / ((1+r)^n − 1)
```

**Where**

* `P` = Loan Amount
* `r` = Monthly Interest Rate
* `n` = Tenure (months)

---

## Running Without Docker

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Data Import

Place Excel files in project root directory:

```
customer_data.xlsx
loan_data.xlsx
```

Then trigger the Celery task to load initial data.

