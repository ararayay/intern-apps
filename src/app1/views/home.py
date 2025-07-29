from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_start=True, set_cookie=True)
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')