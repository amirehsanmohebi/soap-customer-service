from django.core import serializers
from django.shortcuts import render

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from spyne import Iterable
from spyne.application import Application
from spyne.decorator import rpc
from spyne.model.primitive import Unicode, Integer, String, Date
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.service import ServiceBase
from spyne.const import http

from .models import Customer, CustomerService, CustomerModel, CustomerServiceModel

XMLSerializer = serializers.get_serializer("xml")
xml_serializer = XMLSerializer()


class SoapService(ServiceBase):
    @rpc(String(nillable=False), String(nillable=False),
         String(nillable=False), String(nillable=False),
         String(nillable=False), Date(nillable=False), String(nillable=False), _returns=Unicode)
    def add_customer(ctx, first_name, last_name, national_code,
                     father_s_name, birth_certificate_no, birthday, address):
        customer_info_dict = locals()
        for arg in customer_info_dict:
            if customer_info_dict[arg] is None:
                return f'{http.HTTP_400} , {arg} is missing.'

        status, response = Customer.add_customer(first_name=first_name,
                                                 last_name=last_name,
                                                 national_code=national_code,
                                                 father_s_name=father_s_name,
                                                 birth_certificate_no=birth_certificate_no,
                                                 birthday=birthday,
                                                 address=address)
        return f'{status} , {response}'

    @rpc(Integer(nillable=False), String(nillable=False), String(nillable=False), _returns=Unicode)
    def add_service(ctx, customer_id, phone_number, service_name):
        customer_service_info_dict = locals()
        for arg in customer_service_info_dict:
            if customer_service_info_dict[arg] is None:
                return f'{http.HTTP_400} , {arg} is missing.'

        customer = Customer.get_by_id(customer_id=customer_id)
        if customer == 'not found':
            return f'{http.HTTP_404}, customer not found.'
        service_count = customer.services.count()
        if service_count > 10:
            return f'{http.HTTP_409}, maximum number of allowed services reached.'
        status, response = CustomerService.add_service(customer_id=customer_id,
                                                       phone_number=phone_number,
                                                       service_name=service_name)

        return f'{status} , {response}'

    @rpc(Integer(nillable=True), _returns=Iterable(CustomerModel))
    def get_customers(ctx, customer_id):
        customer_service_info_dict = locals()
        queryset = Customer.objects.all()
        if customer_id:
            queryset = queryset.filter(id=customer_id)
        data = []
        for customer in queryset:
            model = CustomerModel(id=customer.id,
                                  first_name=customer.first_name,
                                  last_name=customer.last_name,
                                  national_code=customer.national_code,
                                  father_s_name=customer.father_s_name,
                                  birth_certificate_no=customer.birth_certificate_no,
                                  birthday=customer.birthday,
                                  address=customer.address,
                                  )
            data.append(model)
        return data

    @rpc(Integer(nillable=True), Integer(nillable=True), _returns=Iterable(CustomerServiceModel))
    def get_customer_services(ctx, customer_id, service_id):
        customer_service_info_dict = locals()
        queryset = CustomerService.objects.all()
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        if service_id:
            queryset = queryset.filter(id=service_id)
        data = []
        for customer_service in queryset:
            model = CustomerServiceModel(id=customer_service.id,
                                         customer_id=customer_service.customer_id,
                                         phone_number=customer_service.phone_number,
                                         service_name=customer_service.service_name,
                                         )
            data.append(model)
        return data


soap_app = Application(
    [SoapService],
    tns='django.soap.customer',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
)

django_soap_application = DjangoApplication(soap_app)
customer_soap_application = csrf_exempt(django_soap_application)
