from datetime import date

from django.db import models
from spyne import ComplexModel
from spyne.const import http
from spyne.model.primitive import Unicode, Integer, String, Date

# Create your models here.

# DJANGO MODELS
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_code = models.CharField(max_length=10)
    father_s_name = models.CharField(max_length=50)
    birth_certificate_no = models.CharField(max_length=15)
    birthday = models.DateField()
    address = models.CharField(max_length=500)

    @classmethod
    def add_customer(cls, first_name, last_name, national_code, father_s_name,
                     birth_certificate_no, birthday, address):
        today = date.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        print(age)
        if age < 18:
            return http.HTTP_409, 'Minimal age to subscribe is 18.'
        else:
            customer = cls.objects.create(
                first_name=first_name,
                last_name=last_name,
                national_code=national_code,
                father_s_name=father_s_name,
                birth_certificate_no=birth_certificate_no,
                birthday=birthday,
                address=address
            )
            return http.HTTP_201, f'New customer ID: {customer.id}'

    @classmethod
    def get_by_id(cls, customer_id, **kwargs):
        try:
            return cls.objects.get(id=customer_id, **kwargs)
        except cls.DoesNotExist:
            return 'not found'


class CustomerService(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='services')
    phone_number = models.CharField(max_length=25)
    service_name = models.CharField(max_length=50)


    @classmethod
    def add_service(cls, customer_id, phone_number, service_name):
        customer_service = cls.objects.create(
            customer_id=customer_id,
            phone_number=phone_number,
            service_name=service_name,
        )
        return http.HTTP_201, f'New service ID: {customer_service.id}'

# SPYNE MODELS (USED TO RETURN DATA)


class CustomerModel(ComplexModel):
    id = Integer
    first_name = String
    last_name = String
    national_code = String
    father_s_name = String
    birth_certificate_no = String
    birthday = Date
    address = String


class CustomerServiceModel(ComplexModel):
    id = Integer
    customer_id = Integer
    phone_number = String
    service_name = String
