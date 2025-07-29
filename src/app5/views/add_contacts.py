from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models.bitrix_user_token import BitrixUserToken

from ..file_parsers.factory import get_parser
from ..functions import process_parsed_contacts


@main_auth(on_cookies=True)
def add_contacts(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        # Проверка формата
        if not file.name.endswith(('.csv', '.xlsx')):
            messages.error(request, 'Допустимы только файлы .csv и .xlsx.')
            return render(request, 'home.html')

        parsed_contacts = get_parser(file).parse()

        # Получаем компании и контакты из Битрикса
        bitrix_user_token = request.bitrix_user_token
        batch_result = bitrix_user_token.batch_api_call(methods=[
            ('crm.company.list', {'SELECT': ['ID', 'TITLE']}),
            ('crm.contact.list', {'SELECT': ['ID', 'NAME', 'LAST_NAME', 'PHONE', 'EMAIL', 'COMPANY_ID']}),
        ])
        companies = batch_result['data_0']['result']
        contacts = batch_result['data_1']['result']

        # Создание словаря компаний
        companies_dict = {c['TITLE'].lower(): c['ID'] for c in companies}

        # Создание словаря контактов с ключами вида: имя+фамилия+company_id
        existing_contacts = {}
        for c in contacts:
            key = f"{c['NAME'].lower()}{c['LAST_NAME'].lower()}{str(c.get('COMPANY_ID', '')).lower()}"
            existing_contacts[key] = c

        # Изменение существующих контактов/добавление новых/добавление компании
        message = process_parsed_contacts(parsed_contacts, companies_dict, existing_contacts, bitrix_user_token)

        if message['status'] == 'success':
            messages.success(request, message['message'])
        else:
            messages.error(request, message['message'])

        return render(request, 'home.html')

    return render(request, "app5/add_contacts.html")