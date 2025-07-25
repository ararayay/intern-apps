def employees_to_ids(employees_list: list) -> list:
    # Преобразование списка сотрудников в список их id
    ids_list = []
    for employee in employees_list:
        ids_list.append(int(employee['ID']))
    return ids_list

def departments_to_ids(departments_list: list) -> list:
    # Преобразование списка отделов в список их id
    ids_list = []
    for department in departments_list:
        ids_list.append(int(department['ID']))
    return ids_list

def employees_list_with_heads_and_calls(employees_list: list,
                                        departments_list: list,
                                        departments_with_correct_managers: dict,
                                        calls_list: list) -> list:
    # Преобразование списка сотрудников в словарь
    employees_dict = {}
    for employee in employees_list:
        employees_dict[employee['ID']] = {'name': employee['LAST_NAME'] + ' ' + employee['NAME'],
                                          'calls_count': 0}

    # Добавляю количество звонков в словарь с сотрудниками
    for call in calls_list:
        employees_dict[call['PORTAL_USER_ID']]['calls_count'] += 1

    # Преобразование списка отделов в словарь
    departments_dict = {}
    for department in departments_list:
        departments_dict[department['ID']] = {
            'name': department['NAME'],
            'parent_id': department['PARENT'] if 'PARENT' in department.keys() else None,
            'head_id': str(departments_with_correct_managers[department['ID']][0])
            if department['ID'] in departments_with_correct_managers.keys() else None}

    # Обработка и объединение полученных списков
    result = []
    for employee in employees_list:
        # Если сотрудник работает в нескольких отделах, то должно быть несколько строк
        for department_id in employee['UF_DEPARTMENT']:
            employee_final_dict = {'id': employee['ID'],
                                   'name': employee['LAST_NAME'] + ' ' + employee['NAME'],
                                   'heads': [],
                                   'department': departments_dict[str(department_id)]['name'],
                                   'calls_count': employees_dict[str(employee['ID'])]['calls_count']}

            # Проходимся по каждому руководителю каждого отдела до первого
            while department_id is not None:
                head_id = departments_dict[str(department_id)]['head_id']
                if head_id != employee['ID'] and head_id is not None:
                    employee_final_dict['heads'].append(employees_dict[head_id]['name'])
                department_id = departments_dict[str(department_id)]['parent_id']

            # Преобразуем руководителей в вид для таблицы фронтэнда
            if len(employee_final_dict['heads']) == 0:
                employee_final_dict['heads'] = '-'
            else:
                employee_final_dict['heads'] = ', '.join(employee_final_dict['heads'])

            result.append(employee_final_dict)

    return result