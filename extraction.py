import json
from utils import get_list, get_property, get_inn, search_line


def extract_data(text):
    data = ['ИНН ЮЛ', 'ИНН ФЛ', 'Фамилия:', 'Имя:', 'Отчество:', 'Дата рождения:', 'Адрес постоянной регистрации:', 'E-mail', 'Мобильные', 'Адреса предыдущих регистраций (в том числе временных)', 'Социальные сети', 'Движимое имущество']
    multiple_data = ['ИНН ЮЛ', 'E-mail', 'Мобильные', 'Адреса предыдущих регистраций (в том числе временных)', 'Социальные сети', 'Движимое имущество']
    info = []
    with open('rules.json', 'r', encoding='utf-8',) as file:
        rule_list = json.load(file)
    for item in data:
        if item not in multiple_data:
            if item == 'ИНН ФЛ':
                index = text.rfind('ИНН:')
            else:
                index = text.find(item)
            for call in range(10):
                element = search_line(text, item, index + call)
                if element != '':
                    break
            info.append([item, element.strip()])
        else:
            if item == rule_list['email']:
                rule = rule_list['email_r']
                email_list = get_list(text, item, rule)
                info.append([item, email_list])
            elif item == rule_list['phone']:
                rule = rule_list['phone_r']
                phone_list = get_list(text, item, rule)
                info.append([item, phone_list])
            elif item == rule_list['address']:
                rule = rule_list['address_r']
                address_list = get_list(text, item, rule)
                info.append([item, address_list])
            elif item == rule_list['social']:
                rule = rule_list['social_r']
                social_list = get_list(text, item, rule)
                info.append([item, social_list])
            elif item == rule_list['property']:
                rule = rule_list['property_r']
                property_list = get_property(text, item, rule)
                info.append([item, property_list])
            elif item == rule_list['inn']:
                rule = rule_list['inn_r']
                inn_list = get_inn(text, '3.5 Соучредители', rule)
                info.append([item, inn_list])
    return info