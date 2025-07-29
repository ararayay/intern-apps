from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.signing import Signer

import base64
import os
from dotenv import load_dotenv
from pathlib import Path
import requests


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / '.env')


# Представление для отображения информации о товаре
def product_info(request: HttpRequest, signed_value: str) -> HttpResponse:
    # Преобразование обратно в id товара
    signer = Signer()
    product_id = signer.unsign(signed_value).split(':')[0]

    # Получение из битрикса информации о товаре
    url = f"{os.getenv('WEBHOOK')}catalog.product.get"
    response = requests.get(url, params={"id": product_id})
    data = response.json()['result']['product']

    # Получение фотографии товара
    try:
        relative_url = data['property44'][0]['value']['url']
        full_url = os.getenv('WEBHOOK') + relative_url[6:]

        image_response = requests.get(full_url)
        image_base64 = base64.b64encode(image_response.content).decode('utf-8')
        image_data_url = f"data:image/jpeg;base64,{image_base64}"
    except Exception as e:
        image_data_url = None

    return render(request, 'app2/product_info.html', {
        'product': data,
        'image_url': image_data_url
    })