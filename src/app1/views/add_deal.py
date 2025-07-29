from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib import messages

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.functions.call_list_method import call_list_method

from ..forms import AddDeal


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
            messages.success(request, 'Сделка успешно добавлена!')
        return render(request, 'home.html')

    form = AddDeal()
    return render(request, 'app1/add_deal.html', {"form": form})