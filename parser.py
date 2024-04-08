import sys
import glob
import docx2txt
import csv
from pathlib import Path


def find_single_record(text, item, index):
    restrict = ['\n']
    word = ''
    start = index + len(item)
    for i in range(200):
        symbol = text[start + i]
        if symbol in restrict:
            break
        word += symbol
    return word

def find_line(text, item, start, end):
    line = ''
    count = 0
    for i in range(start, end):
        symbol = text[start + count]
        line += symbol
        count += 1
    return line

def get_email(text, item):
    start = text.find(item)
    end = text.find('3.	Люди имеющие отношения к фигуранту')
    element = find_line(text, item, start, end)
    extracted_data = element.split('\n')
    extracted_data.remove('E-mail')
    email_list = [i for i in extracted_data if i != '']
    return email_list

def get_phone(text, item):
    start = text.find(item)
    end = text.find('E-mail')
    element = find_line(text, item, start, end)
    extracted_data = element.split('\n')
    extracted_data.remove('Мобильные')
    phone_list = [i for i in extracted_data if i != '']
    return phone_list

def get_address(text, item):
    start = text.find(item)
    end = text.find('2.	Телефоны имеющие отношения к фигуранту')
    element = find_line(text, item, start, end)
    extracted_data = element.split('\n')
    extracted_data.remove('Адреса предыдущих регистраций (в том числе временных)')
    address_list = [i for i in extracted_data if i != '']
    return address_list

def get_address(text, item):
    start = text.find(item)
    end = text.find('2.	Телефоны имеющие отношения к фигуранту')
    element = find_line(text, item, start, end)
    extracted_data = element.split('\n')
    extracted_data.remove('Адреса предыдущих регистраций (в том числе временных)')
    address_list = [i for i in extracted_data if i != '']
    return address_list

def get_social(text, item):
    start = text.find(item)
    end = text.find('13. Счета')
    element = find_line(text, item, start, end)
    extracted_data = element.split('\n')
    extracted_data.remove('Социальные сети')
    social_list = [i for i in extracted_data if i != '']
    return social_list

def get_property(text, item):
    start = text.rfind(item)
    end = text.find('Раздел четвертый')
    element = find_line(text, item, start, end)
    extracted_data = element.split('\n')
    property_list = []
    for elem in extracted_data:
        if elem[:8] == 'Госномер':
            property_list.append(elem)
    return property_list

def get_inn(text, item):
    start = text.find(item)
    end = text.find('4.	Близкие родственники')
    element = find_line(text, item, start, end)
    extracted_data = element.split('\n')
    property_list = []
    for elem in extracted_data:
        if 'ИНН' in elem:
            property_list.append(elem)
    return property_list

def extract_data(text):
    data = ['ИНН ЮЛ', 'ИНН ФЛ', 'Фамилия:', 'Имя:', 'Отчество:', 'Дата рождения:', 'Адрес постоянной регистрации:', 'E-mail', 'Мобильные', 'Адреса предыдущих регистраций (в том числе временных)', 'Социальные сети', 'Движимое имущество']
    multiple_data = ['ИНН ЮЛ', 'E-mail', 'Мобильные', 'Адреса предыдущих регистраций (в том числе временных)', 'Социальные сети', 'Движимое имущество']
    info = []
    for item in data:
        if item not in multiple_data:
            if item == 'ИНН ФЛ':
                index = text.rfind('ИНН:')
            else:
                index = text.find(item)
            for call in range(10):
                element = find_single_record(text, item, index + call)
                if element != '':
                    break
            info.append([item, element.strip()])
        else:
            if item == 'E-mail':
                email_list = get_email(text, item)
                info.append([item, email_list])
            elif item == 'Мобильные':
                phone_list = get_phone(text, item)
                info.append([item, phone_list])
            elif item == 'Адреса предыдущих регистраций (в том числе временных)':
                address_list = get_address(text, item)
                info.append([item, address_list])
            elif item == 'Социальные сети':
                social_list = get_social(text, item)
                info.append([item, social_list])
            elif item == 'Движимое имущество':
                property_list = get_property(text, item)
                info.append([item, property_list])
            elif item == 'ИНН ЮЛ':
                inn_list = get_inn(text, '3.5 Соучредители')
                info.append([item, inn_list])

    return info

def create_csv(data):
    with open('demo.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for i in range(len(data)):
            writer.writerow(
                [data[i][0], data[i][1]],
            )

def processing(textfile):
    data = extract_data(textfile)
    create_csv(data)

def main():
    root_path = root_path = Path(sys.modules['__main__'].__file__).resolve().parents[0]
    res = [f for f in Path(root_path).glob('**/*.docx')]
    for filepath in res:
        textfile = docx2txt.process(filepath)
        processing(textfile)


if __name__ == '__main__':
    main()