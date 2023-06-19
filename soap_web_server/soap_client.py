# soap_client.py
# coding=utf-8

from suds.client import Client
from suds.cache import NoCache
from datetime import date

my_client = Client('http://127.0.0.1:8000/soap_service/customers/?WSDL', cache=NoCache())

# ADD CUSTOMER
print('Function Add Customer: ', my_client.service.add_customer('Mohamad',
                                                         'najarzade',
                                                         '0674690494',
                                                         'heshmat',
                                                         '0674690494',
                                                         date(year=1990, month=1, day=25),
                                                         'Azadi St, yadegar emam, No4'
                                                         ))
# ADD SERVICE
print('Function Add Customer: ', my_client.service.add_service(1,
                                                         '09056585478',
                                                         'service1',
                                                         ))

# GET CUSTOMER [RETURNS A LIST OF CUSTOMERS AS DEFAULT, BUT ALSO ACCEPTS CUSTOMER_ID SEARCH]
print('Function Get Customer(s) Without customer_id param: ', my_client.service.get_customers())
print('Function Get Customer(s) With customer_id param: ', my_client.service.get_customers(1))

# GET CUSTOMER SERVICE [RETURNS A LIST OF CUSTOMER SERVICES AS DEFAULT, BUT ALSO ACCEPTS CUSTOMER_ID AND SERVICE_ID
# SEARCH]
print('Function Get Customer Service(s) Without customer_id and service_id param: ', my_client.service.get_customer_services())
print('Function Get Customer Service(s) With customer_id and Without service_id param: ', my_client.service.get_customer_services(1))
print('Function Get Customer Service(s) Without customer_id and With service_id param: ', my_client.service.get_customer_services(None, 2))
