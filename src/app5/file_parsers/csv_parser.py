import csv
import io
from .base import BaseParser

class CSVParser(BaseParser):
    def parse(self):
        decoded = self.file.read().decode('windows-1251')
        io_string = io.StringIO(decoded)
        reader = csv.DictReader(io_string, delimiter=';')

        contacts = []
        for row in reader:
            contacts.append({
                'name': row['имя'].strip(),
                'last_name': row['фамилия'].strip(),
                'phone': row['номер телефона'].strip(),
                'email': row['почта'].strip(),
                'company': row['компания'].strip()
            })
        return contacts
