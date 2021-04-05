import datetime


def iso_to_date(iso_str: str):
    """Convert a date string with iso formating to a datetime date object"""
    if not iso_str:
        return None
    return datetime.date(*map(int, iso_str.split('-')))
