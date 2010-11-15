from flaskext.babel import format_date, format_datetime
# filters.py
def format_datetime(date=None, format=None):
    """the `datetimeformat` filter"""
    return format_datetime(date, 'long')

def format_date(date=None, format=None):
    return format_date(date, 'long')

