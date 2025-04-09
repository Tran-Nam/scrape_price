import gspread 


gc = gspread.service_account('secret.json')
try:
    sheet = gc.open('Car Price')
except gspread.exceptions.SpreadsheetNotFound:
    sheet = gc.create('Car Price')
    
def convert_to_dict(values):
    d = {}
    for v in values:
        d[v[0]] = v[-1]
    return d

def write(title: str, data: list, clear: bool = True):
    try:
        worksheet = sheet.worksheet(title=title)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=title, 
                                        rows=len(data), 
                                        cols=len(data[0]))
    # get content of worksheet
    existed_data = worksheet.get_all_values()
    if len(existed_data[0]) != 0:
        existed_data = existed_data[1:] # discard the header
        data_dict = convert_to_dict(values=data[1:])
        col_data = [[f'{datetime.now().strftime("%d-%m-%Y")}']]
        for v in existed_data:
            col_data.append([data_dict[v[0]]])
        worksheet.add_cols(cols=1)
        start_row = 1
        end_row = len(col_data) + 1
        col_index = len(existed_data[0]) + 1
        range_label = f"{chr(ord('A') + col_index - 1)}{start_row}:{chr(ord('A') + col_index - 1)}{end_row}"
        worksheet.update(range_label, col_data)
    else:
        if clear:
            worksheet.clear()
        worksheet.insert_rows(data)
    return 1