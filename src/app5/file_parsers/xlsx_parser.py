import openpyxl
from .base import BaseParser

class XLSXParser(BaseParser):
    def parse(self):
        wb = openpyxl.load_workbook(self.file, read_only=True)
        sheet = wb.active

        contacts = []
        for i, row in enumerate(sheet.iter_rows(values_only=True)):
            if i == 0:
                continue

            name = row[0]
            last_name = row[1]
            phone = row[2]
            email = row[3]
            company = row[4]

            contact = {
                'name': str(name).strip(),
                'last_name': str(last_name).strip(),
                'phone': str(phone).strip(),
                'email': str(email).strip(),
                'company': str(company).strip(),
            }
            contacts.append(contact)

        return contacts
