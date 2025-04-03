import gspread 


gc = gspread.service_account('secret.json')
try:
    sheet = gc.open('Car Price')
except gspread.exceptions.SpreadsheetNotFound:
    sheet = gc.create('Car Price')

def write(title: str, data: list, clear: bool = True):
    try:
        worksheet = sheet.worksheet(title=title)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=title, 
                                        rows=len(data), 
                                        cols=len(data[0]))
    if clear:
        worksheet.clear()
    worksheet.insert_rows(data)
    return 1