from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.functions.call_list_method import call_list_method

from ..functions import format_date


@main_auth(on_cookies=True)
def last_deals(request: HttpRequest) -> HttpResponse:
    result = call_list_method(bx_token=request.bitrix_user_token,
                              method='crm.deal.list',
                              fields={
                                  'FILTER': {'CLOSED': 'N'},
                                  'ORDER': {'DATE_CREATE': 'DESC'},
                                  'SELECT': ['TITLE', 'STAGE_ID', 'OPPORTUNITY', 'DATE_CREATE',
                                             'BEGINDATE', 'UF_CRM_1752828792635']
                              })
    last_deals = result[:10]

    # Предобработка полей
    for deal in last_deals:
        deal['DATE_CREATE'] = format_date(deal['DATE_CREATE'])
        deal['BEGINDATE'] = format_date(deal['BEGINDATE'])
        if deal['UF_CRM_1752828792635']:
            deal['UF_CRM_1752828792635'] = deal['UF_CRM_1752828792635'] + '%'

    return render(request, 'app1/last_deals.html', {'last_deals': last_deals})