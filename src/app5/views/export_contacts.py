from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models.bitrix_user_token import BitrixUserToken

from ..functions import csv_file_create, xlsx_file_create
from datetime import datetime, timedelta


@main_auth(on_cookies=True)
def export_contacts(request: HttpRequest) -> HttpResponse:
    bitrix_user_token = request.bitrix_user_token
    companies = bitrix_user_token.batch_api_call(methods=[
        ('crm.company.list', {'SELECT': ['ID', 'TITLE']})
    ])['data_0']['result']

    if request.method == 'POST':
        # Преобразование списка компаний в словари
        companies_id_dict = {c['ID']: c['TITLE'] for c in companies}
        companies_title_dict = {c['TITLE']: c['ID'] for c in companies}

        # Получение значений фильтров
        company = request.POST.get('company')
        time = request.POST.get('time')
        export_format = request.POST.get('format', 'csv')

        # Дополнительные фильтры к запросу
        filters = {}
        if time != 'all':
            filters['>DATE_CREATE'] = (datetime.now() - timedelta(days=1)).isoformat()
        if company != 'all':
            filters['COMPANY_ID'] = companies_title_dict.get(company)

        # Запрос
        contacts = bitrix_user_token.batch_api_call(methods=[
            ('crm.contact.list', {
                'SELECT': ['NAME', 'LAST_NAME', 'PHONE', 'EMAIL', 'COMPANY_ID'],
                'FILTER': filters
            })
        ])['data_0']['result']

        # Формирование файла
        if export_format == 'xlsx':
            return xlsx_file_create(contacts, companies_id_dict)
        elif export_format == 'csv':
            return csv_file_create(contacts, companies_id_dict)

    # Преобразование списка компаний в список с названиями для вариантов фильтра
    companies_list = [c['TITLE'] for c in companies]
    context = {'companies_list': companies_list}

    return render(request, "app5/export_contacts.html", context)