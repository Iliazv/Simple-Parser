import json
import os
import sys
import glob
import docx2txt
import csv
from pathlib import Path
# import utils
from handlers import processing


def main():
    root_path = Path(sys.modules['__main__'].__file__).resolve().parents[0]
    document_path = os.path.join(root_path, 'documents/')
    res = [f for f in Path(document_path).glob('**/*.docx')]
    if res == []:
        print('Неверно указан путь или отсутствуют файлы формата docx')
    for filepath in res:
        textfile = docx2txt.process(filepath)
        processing(textfile, filepath)


if __name__ == '__main__':
    main()