from django.http import HttpResponse
import csv
from openpyxl import Workbook
import io


def process_parsed_contacts(parsed_contacts, companies_dict, existing_contacts, bitrix_user_token):
    try:
        for contact in parsed_contacts:
            company_title = contact['company'].lower()
            company_id = companies_dict.get(company_title)

            if not company_id:
                continue  # Пропускаем, если такой компании нет

            key = f"{contact['name'].lower()}{contact['last_name'].lower()}{str(company_id)}"
            existing = existing_contacts.get(key)

            if existing:
                update_fields = {}

                # Обновление телефона
                if 'PHONE' not in existing.keys():
                    update_fields['PHONE'] = [{'VALUE': contact['phone'], 'VALUE_TYPE': 'WORK'}]
                elif existing['PHONE'][0]['VALUE'] != contact['phone']:
                    update_fields['PHONE'] = [{'VALUE': contact['phone'], 'VALUE_TYPE': 'WORK'}]

                # Обновление email
                if 'EMAIL' not in existing.keys():
                    update_fields['EMAIL'] = [{'VALUE': contact['email'], 'VALUE_TYPE': 'WORK'}]
                elif existing['PHONE'][0]['VALUE'] != contact['email']:
                    update_fields['EMAIL'] = [{'VALUE': contact['email'], 'VALUE_TYPE': 'WORK'}]

                if update_fields:
                    bitrix_user_token.batch_api_call(methods=[
                        ('crm.contact.update', {
                            'id': existing['ID'],
                            'fields': update_fields
                        })])

            else:
                # Добавление нового контакта
                bitrix_user_token.batch_api_call(methods=[
                    ('crm.contact.add', {'fields': {
                        'NAME': contact['name'],
                        'LAST_NAME': contact['last_name'],
                        'PHONE': [{'VALUE': contact['phone'], 'VALUE_TYPE': 'WORK'}],
                        'EMAIL': [{'VALUE': contact['email'], 'VALUE_TYPE': 'WORK'}],
                        'COMPANY_ID': company_id
                    }})])

        return {'status': 'success',
                'message': "Контакты успешно добавлены и/или изменены!"}

    except Exception as e:
        return {'status': 'error',
                'message': f"Произошла ошибка при обработке контактов: {e}"}

def csv_file_create(contacts, companies_id_dict):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['имя', 'фамилия', 'номер телефона', 'почта', 'компания'])

    for contact in contacts:
        name = contact.get('NAME', '')
        last_name = contact.get('LAST_NAME', '')
        phone = contact.get('PHONE', [{}])[0].get('VALUE', '')
        email = contact.get('EMAIL', [{}])[0].get('VALUE', '')
        company_title = companies_id_dict.get(contact.get('COMPANY_ID', ''), '')

        writer.writerow([name, last_name, phone, email, company_title])

    return response

def xlsx_file_create(contacts, companies_id_dict):
    wb = Workbook()
    ws = wb.active
    ws.title = "Контакты"
    ws.append(['имя', 'фамилия', 'номер телефона', 'почта', 'компания'])

    for contact in contacts:
        name = contact.get('NAME', '')
        last_name = contact.get('LAST_NAME', '')
        phone = contact.get('PHONE', [{}])[0].get('VALUE', '')
        email = contact.get('EMAIL', [{}])[0].get('VALUE', '')
        company_title = companies_id_dict.get(contact.get('COMPANY_ID', ''), '')

        ws.append([name, last_name, phone, email, company_title])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="export.xlsx"'
    return response