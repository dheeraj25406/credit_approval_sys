import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR=Path(__file__).resolve().parent.parent

SECRET_KEY=os.getenv("SECRET_KEY")
DEBUG=os.getenv("DEBUG")=="1"
ALLOWED_HOSTS=["*"]

INSTALLED_APPS=[
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'rest_framework',
'core',
]

MIDDLEWARE=[
'django.middleware.security.SecurityMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF='credit_system.urls'

TEMPLATES=[{
'BACKEND':'django.template.backends.django.DjangoTemplates',
'DIRS':[],
'APP_DIRS':True,
'OPTIONS':{'context_processors':[
'django.template.context_processors.debug',
'django.template.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
]},
}]

WSGI_APPLICATION='credit_system.wsgi.application'

DATABASES={
'default':{
'ENGINE':'django.db.backends.postgresql',
'NAME':os.getenv("POSTGRES_DB"),
'USER':os.getenv("POSTGRES_USER"),
'PASSWORD':os.getenv("POSTGRES_PASSWORD"),
'HOST':os.getenv("POSTGRES_HOST"),
'PORT':os.getenv("POSTGRES_PORT"),
}
}

AUTH_PASSWORD_VALIDATORS=[]

LANGUAGE_CODE='en-us'
TIME_ZONE='UTC'
USE_I18N=True
USE_TZ=True
STATIC_URL='/static/'

DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'

CELERY_BROKER_URL='redis://redis:6379/0'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TASK_SERIALIZER='json'