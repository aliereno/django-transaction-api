# Experimental Transaction API with Django

## Run:

```
# Project runs on Docker and Docker-Compose
make up
```
## Migration:

```
make makemigrations
make migrate
```

## Tech stack
- Django
- DjangoRestFramework
- Celery
- Redis

## Features
- Organization, User, Transaction Models
- Deposit & Withdraw Money endpoints
- Authentication for Users belong in Organization
- Endpoint Permissions for Organization Users
- Organization Users can see all transactions, can Approve/Reject transactions 
- Async Support with [**Celery**](https://docs.celeryq.dev/en/stable/)
- Celery Monitoring with [**Flower**](https://github.com/mher/flower)(*http://localhost:5555/*)
- Transactions CSV Export in Admin Dashboard

## Documentation for API Endpoints

All URIs are relative to *http://localhost:7779/api/v1/*


Desc | Method | HTTP request
------------ | ------------- | -------------
*Authenticate Organization Users*  | [**OrganizationAuthenticateView**](https://github.com/aliereno/django-transaction-api/blob/main/core/views/organization.py#L39-L58) | **POST** /organization/\<str:organization_id>/auth
*Observe Organization's Transactions* | [**OrganizationDashboardView**](https://github.com/aliereno/django-transaction-api/blob/main/core/views/organization.py#L61-L82) | **GET** /organization/\<str:organization_id>/dashboard
*Deposit URI for Organization Customers* | [**OrganizationDepositView**](https://github.com/aliereno/django-transaction-api/blob/main/core/views/organization.py#L85-L99) | **POST** /organization/\<str:organization_id>/deposit
*Withdrawal URI for Organization Customers* | [**OrganizationWithdrawalView**](https://github.com/aliereno/django-transaction-api/blob/main/core/views/organization.py#L102-L116) | **POST** /organization/\<str:organization_id>/withdrawal
*Show Organization Requested Transactions' Detail* | [**OrganizationApprovementHandleView**](https://github.com/aliereno/django-transaction-api/blob/main/core/views/organization.py#L119-L159) | **GET** /organization/\<str:organization_id>/approvements/\<str:approvement_id>
*Handle(Approve or Reject) Organization Requested Transaction* | [**OrganizationApprovementHandleView**](https://github.com/aliereno/django-transaction-api/blob/main/core/views/organization.py#L119-L159) | **POST** /organization/\<str:organization_id>/approvements/\<str:approvement_id>
*Show Organization Requested Transactions' List* | [**OrganizationApprovementsView**](https://github.com/aliereno/django-transaction-api/blob/main/core/views/organization.py#L162-L176) | **GET** /organization/\<str:organization_id>/approvements
