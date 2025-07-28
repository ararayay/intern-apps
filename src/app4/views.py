from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.functions.call_list_method import call_list_method

from .functions import get_coordinates

import os
from dotenv import load_dotenv

load_dotenv('.env')


@main_auth(on_cookies=True)
def companies_map(request: HttpRequest) -> HttpResponse:
    companies = call_list_method(bx_token=request.bitrix_user_token,
                                 method='crm.company.list',
                                 fields={
                                     'SELECT': ['ID', 'TITLE']
                                 })

    addresses = call_list_method(bx_token=request.bitrix_user_token,
                                 method='crm.address.list',
                                 fields={
                                     'SELECT': ['ENTITY_ID', 'ADDRESS_1', 'CITY']
                                 })

    YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")

    # Объединяем данные компаний и адресов
    companies_with_coordinates = []
    if companies and addresses:
        # Создаем словарь адресов по ENTITY_ID для быстрого поиска
        address_dict = {}
        for address in addresses:
            entity_id = address.get('ENTITY_ID')
            if entity_id:
                address_dict[entity_id] = address

        # Объединяем компании с их адресами
        for company in companies:
            company_id = company.get('ID')
            if company_id and company_id in address_dict:
                address = address_dict[company_id]
                full_address = f"{address.get('ADDRESS_1', '')}, {address.get('CITY', '')}"
                coordinates = get_coordinates(full_address, YANDEX_API_KEY)

                companies_with_coordinates.append({
                    'id': company_id,
                    'title': company.get('TITLE', ''),
                    'address': full_address,
                    'coordinates': coordinates
                })

    context = {
        'YANDEX_API_KEY': YANDEX_API_KEY,
        'companies_json': companies_with_coordinates
    }

    return render(request, "app4/map.html", context)