from datetime import datetime


def format_date(date):
    return datetime.fromisoformat(date).strftime('%d.%m.%Y %H:%M')