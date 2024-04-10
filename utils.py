import os
import sys
import csv
from pathlib import Path


def search_line(text, item, index):
    restrict = ['\n']
    word = ''
    start = index + len(item)
    for i in range(200):
        try:
            symbol = text[start + i]
        except: symbol = ''
        if symbol in restrict:
            break
        word += symbol
    return word

def search_block(text, item, start, end):
    line = ''
    for i in range(start, end):
        try:
            symbol = text[i]
        except: symbol = ''
        line += symbol
    return line

def get_list(text, item, rule):
    data_list = []
    start = text.find(item)
    end = text.find(rule)
    element = search_block(text, item, start, end)
    extracted_data = element.split('\n')
    if item in extracted_data:
        extracted_data.remove(item)
    data_list = [i for i in extracted_data if i != '']
    if item == 'E-mail' or item == 'Адреса предыдущих регистраций (в том числе временных)':
        data_list = data_list[:-1]
    return data_list

def get_property(text, item, rule):
    start = text.rfind(item)
    end = text.find(rule)
    element = search_block(text, item, start, end)
    extracted_data = element.split('\n')
    property_list = []
    for elem in extracted_data:
        if elem[:8] == 'Госномер':
            property_list.append(elem)
    return property_list

def get_inn(text, item, rule):
    start = text.find(item)
    end = text.rfind(rule)
    element = search_block(text, item, start, end)
    extracted_data = element.split('\n')
    property_list = []
    for elem in extracted_data:
        if 'ИНН' in elem:
            property_list.append(elem)
    return property_list