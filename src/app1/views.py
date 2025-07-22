from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.functions.call_list_method import call_list_method
from .forms import AddDeal


@main_auth(on_start=True, set_cookie=True)
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')

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
        deal['DATE_CREATE'] = deal['DATE_CREATE'][:10] + ' ' + deal['DATE_CREATE'][11:16]
        deal['BEGINDATE'] = deal['BEGINDATE'][:10] + ' ' + deal['BEGINDATE'][11:16]
        if deal['UF_CRM_1752828792635']:
            deal['UF_CRM_1752828792635'] = deal['UF_CRM_1752828792635'] + '%'

    return render(request, 'last_deals.html', {'last_deals': last_deals})

@main_auth(on_cookies=True)
def add_deal(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AddDeal(request.POST)
        if form.is_valid():
            result = call_list_method(
                bx_token=request.bitrix_user_token,
                method='crm.deal.add',
                fields={'FIELDS': {
                    'TITLE': form.cleaned_data['title'],
                    'OPPORTUNITY': form.cleaned_data['sum'],
                    'UF_CRM_1752828792635': form.cleaned_data['probability']
                }}
            )
        return render(request, 'home.html')

    form = AddDeal()
    return render(request, 'add_deal.html', {"form": form})