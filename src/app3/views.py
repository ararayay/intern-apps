from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.functions.call_list_method import call_list_method

from .functions import employees_to_ids, departments_to_ids, employees_list_with_heads_and_calls
from datetime import datetime, timedelta
import random


@main_auth(on_cookies=True)
def employees(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    # Получаю список сотрудников, нужные поля: ID, NAME, LAST_NAME, UF_DEPARTMENT
    employees_list = call_list_method(bx_token=request.bitrix_user_token,
                                      method='user.get',
                                      fields={
                                          'FILTER': {'USER_TYPE': 'employee'},
                                          'ACTIVE': True
                                      })

    if request.method == "GET":
        # Получаю список отделов с руководителями, поля: ID, NAME, PARENT, UF_HEAD
        departments_list = call_list_method(bx_token=request.bitrix_user_token,
                                            method='department.get')

        # Получаю словарь с корректными руководителями отдела
        '''
        При добавлении второго руководителя в отдел и его удалении предыдущий метод (department.get)
        возвращает информацию, как будто у отдела нет руководителя вообще (при условии, что предыдущий руководитель
        остался). Так что, чтобы обеспечить достоверность данных, использую дополнительный метод
        im.department.managers.get, у которого такого бага нет.
        '''
        departments_with_correct_managers = call_list_method(bx_token=request.bitrix_user_token,
                                                             method='im.department.managers.get',
                                                             fields={
                                                                 'ID': departments_to_ids(departments_list)
                                                             })

        # Дата день назад
        day_ago = (datetime.now() - timedelta(days=1)).isoformat()
        # Получаю список звонков
        calls_list = call_list_method(bx_token=request.bitrix_user_token,
                                      method='voximplant.statistic.get',
                                      fields={
                                          'FILTER': {'CALL_TYPE': 1,
                                                     '>CALL_DURATION': 60,
                                                     '>CALL_START_DATE': day_ago}
                                      })

        result = employees_list_with_heads_and_calls(employees_list, departments_list, departments_with_correct_managers, calls_list)

        return render(request, "app3/employees.html", {'employees': result})

    # Генерация звонков, если нажата кнопка (то есть отправлен POST-запрос)
    ids_list = employees_to_ids(employees_list)

    for i in range(4):
        user_id = random.choice(ids_list)

        try:
            # Создание звонка
            make_call = call_list_method(bx_token=request.bitrix_user_token,
                                         method='telephony.externalcall.register',
                                         fields={
                                             'USER_PHONE_INNER': 1,
                                             'USER_ID': user_id,
                                             'PHONE_NUMBER': 1,
                                             'TYPE': 1,
                                             'SHOW': 0 # Чтобы не открывалась карточка звонка
                                         })

            # Закрытие звонка
            close_call = call_list_method(bx_token=request.bitrix_user_token,
                                          method='telephony.externalcall.finish',
                                          fields={
                                              'CALL_ID': make_call['CALL_ID'],
                                              'USER_ID': user_id,
                                              'DURATION': random.randint(61, 300)
                                          })
        except Exception as e:
            continue

    return redirect('employees')