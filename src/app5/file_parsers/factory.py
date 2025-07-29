from .csv_parser import CSVParser
from .xlsx_parser import XLSXParser

def get_parser(file):
    if file.name.endswith('.csv'):
        return CSVParser(file)
    elif file.name.endswith('.xlsx'):
        return XLSXParser(file)
    else:
        raise ValueError('Unsupported file format')
