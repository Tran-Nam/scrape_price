import traceback 
import requests
from bs4 import BeautifulSoup

from writer import write

 
def extract_row(row, length=None, skip_indexs=[]):
    cells = row.find_all(['td', 'th'])
    if length is None:
        length = len(cells)
    avail_ids = [i for i in range(length) if i not in skip_indexs]
    output_list = ['' for _ in range(length)]
    output_skip_ids = []
    for i, cell in enumerate(cells):
        if int(cell.get("rowspan", 1)) > 1:
            output_skip_ids.append(i)
        output_list[avail_ids[i]] = cell.text.strip()
    return output_list, output_skip_ids

def get_soup(url):
    return BeautifulSoup(requests.get(url).content, 'html.parser')

def check_overall_price(title):
    accepted_title = [ 
        "TIN BÁN XE", 
        "BẢNG GIÁ XE", 
    ]
    is_overall = False 
    for a_t in accepted_title:
        if a_t in title:
            is_overall = True 
            break 
    return is_overall

def get_car_brand(title):
    accepted_brand = [
        "TOYOTA", 
        "HYUNDAI", 
        "HONDA",
        "MAZDA", 
        "KIA", 
        "FORD", 
        "BMW", 
        "MERCEDES", 
        "MITSUBISHI", 
        "NISSAN", 
        "PEUGEOT", 
        "SUZUKI", 
        "VINFAST"
    ]
    for brand in accepted_brand:
        if brand in title:
            return brand 
    return None

url = 'https://bonbanh.com/gia-xe-oto'
soup = get_soup(url)

processed_title = []

for c_brand in soup.find_all('h3'):
    c_brand_url = c_brand.a 
    if c_brand_url is None:
        continue 
    c_brand_soup = get_soup(c_brand_url.get('href'))
    for c_type in c_brand_soup.find_all(['h3', 'h2'], attrs={"class": "c_title"}):
        c_type_url = c_type.a
        if c_type_url is None:
            continue 
        c_type_soup = get_soup(c_type_url.get('href'))
        for table in c_type_soup.find_all('table'):
            tr_tabs = table.find_all('tr')
            if len(tr_tabs[0].find_all(['td', 'th'])) <= 1:
                title = tr_tabs[0].text.strip().replace('/', '-').upper()
                if len(title) == 0:
                    continue
                header, _ = extract_row(tr_tabs[1])
                start_i = 2
            else:
                title = c_type.text.strip().replace('/', '-').upper()
                header, _ = extract_row(tr_tabs[0])
                start_i = 1
            if not check_overall_price(title=title):
                continue
            if title in processed_title:
                continue
            processed_title.append(title)
            length = len(header)
            values = []
            skip_ids = []
            for row in tr_tabs[start_i:]:
                try:
                    value, skip_ids = extract_row(row, length=length, skip_indexs=skip_ids)
                    values.append(value)
                except:
                    pass

            data = [header] + values 
            car_brand = get_car_brand(title=title)
            if car_brand is None:
                continue
            write(title=car_brand, data=data)