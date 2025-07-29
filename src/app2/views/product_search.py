from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.signing import Signer

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.functions.call_list_method import call_list_method

from ..forms import GenerateQR
import qrcode, io, base64
import uuid


@main_auth(on_cookies=True)
def product_search(request: HttpRequest) -> HttpResponse|JsonResponse:
    # Если пользователь вводит значения для поиска
    if request.GET.get('q') is not None:
        query = request.GET.get('q', '')
        if not query:
            return JsonResponse([], safe=False)

        result = call_list_method(
            bx_token=request.bitrix_user_token,
            method='catalog.product.list',
            fields={'filter': {'name': f'%{query}%',
                               'iblockId': 14}, # 14 - "Товарный каталог CRM", 16 - "Товарный каталог CRM (предложения)"
                    'select': ['id', 'iblockId', 'name'],
                    'start': -1})

        # Для получения информации о каталогах товаров
        # result = call_list_method(
        #     bx_token=request.bitrix_user_token,
        #     method='catalog.catalog.list'
        # )
        # print(result)

        products = [
            {"id": product_info["id"], "name": product_info["name"]}
            for product_info in result['products']
        ]
        return JsonResponse(products, safe=False)

    # Если пользователь выбрал название товара и отправил форму
    if request.method == 'POST':
        form = GenerateQR(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            signer = Signer()
            unique_str = f"{product_id}:{uuid.uuid4()}"
            # id зашифровывается
            signed_value = signer.sign(unique_str)
            # Формируется ссылка на локальный сервер
            product_url = f'http://localhost:8000/products/product/{signed_value}/'

            # Генерируется QR-код
            qr = qrcode.make(product_url)
            # Создаётся "виртуальный файл" в памяти, чтобы не сохранять его на жестком диске
            buffer = io.BytesIO()
            # Сохранение
            qr.save(buffer, format='PNG')
            # Превращение QR-кода в строку для отображения в html
            img_str = base64.b64encode(buffer.getvalue()).decode()

            # Передаем строку с QR-кодом в шаблон как data URI
            qr_data_uri = f"data:image/png;base64,{img_str}"

            return render(request, 'app2/product_qr.html',{'qr_code': qr_data_uri,
                                                           'url': product_url})

    # Если пользователь запросил страницу с формой
    else:
        form = GenerateQR()

    return render(request, 'app2/product_search.html', {"form": form})