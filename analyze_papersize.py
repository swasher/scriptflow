#!/usr/bin/python
#coding: utf-8
__author__ = 'Алексей'

from genericpath import isfile
from classes import PrintingPress
from subprocess import Popen, PIPE


def analyze_papersize(pdfname):
    """
    Функция возвращает словарь, в котором ключ - номер страницы, значения: машина, ширина листа, высота листа.
    Если возвращается None - файл не найден
    Если возвращается пустой словарь - файл не Сигновский, нет инфы о страницах.
    :param pdfname:
    :return:
    """

    if not isfile(pdfname):
        papersizes = None
        return papersizes

    pdftotext_command = r"pdftotext {input} - | grep -E '({machines})'"\
        .format(input=pdfname, machines='|'.join([i.name for i in PrintingPress._registry]))  # объяснение см. test1 ниже
    pdftotext_result = Popen(pdftotext_command, shell=True, stdin=PIPE, stdout=PIPE).stdout.read().splitlines()

    papersizes = {}

    for index, value in enumerate(pdftotext_result):
        page_number = index + 1
        page_param = value.split()  # return somthing like ['Speedmaster', '900,0', 'x', '640,0']
        page_machine = page_param[0]
        page_paper_x = int(float(page_param[1].replace(',', '.')))  # В Сигне число имеет запятую вместо точки
        page_paper_y = int(float(page_param[3].replace(',', '.')))
        papersizes[page_number] = (page_machine, page_paper_x, page_paper_y)

    return papersizes


def test():
    """
    Пример парсинга результата. Выполняется проверка на пустой словарь (файл не Сигновский, нет инфы о размере страниц),
    и на словарь is None - файл не найден.
    """
    f = '000_TEST_Dom_Leonov.pdf', '000_TEST_Pla_Leonov.pdf', '000_TEST_Spe_Leonov.pdf', '0540_1.pdf', \
        '0540_2.pdf', 'test_manypages.pdf', 'test_cyan_50perc_Admin.pdf', 'HD_2pages_CM+CPant_Admin.pdf', \
        '0045_Ivanovka_Kniga_Leonov_Inner.pdf'
    #f = ['SIGNA_A1-100C100M---A250C50P_Admin.pdf']

    for pdf in f:
        print '\n\n'
        pdf = 'test_pdf/' + pdf
        print pdf
        print '---------------------------'


        paper_size_dic = analyze_papersize(pdf)
        print 'DIC=', paper_size_dic

        if paper_size_dic:
            for page_number, p in paper_size_dic.iteritems():
                print 'Page', page_number, ':', "Machine: {} width {} heigh {}".format(p[0], p[1], p[2])
        else:
            if paper_size_dic == {}:
                print 'Cant parse {}'.format(pdf)
            elif paper_size_dic is None:
                print 'Cant find {}'.format(pdf)
            else:
                print 'Unknown error'


def test1():

    # Используем генератор для получения всех названий машин
    a = [i.name for i in PrintingPress._registry]
    print(a)
    # >>> ['Dominant', 'Speedmaster', 'Planeta']

    # Объеденяем через вертикальный слеш
    b = '|'.join(a)
    print(b)
    # >>> Dominant|Speedmaster|Planeta

if __name__ == '__main__':
    test1()