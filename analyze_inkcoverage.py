#!/usr/bin/python
#coding: utf-8
__author__ = 'Алексей'

from subprocess import Popen, PIPE


def analyze_inkcoverage(pdfname):
    """
    Анализ заполнения краски
    :param pdfname: pdfname(str)
        пусть к файлу pdf
    :return: inks(dict)
        словарь, в котором ключ - номер страницы, значение - список из четырех float цифр, в процентах
    """

    gs_command = r"gs -q -o - -sProcessColorModel=DeviceCMYK -sDEVICE=ink_cov {}".format(pdfname)
    gs_result = Popen(gs_command, shell=True, stdin=PIPE, stdout=PIPE).stdout.read().splitlines()

    inks = {}

    for index, s in enumerate(gs_result):
        args = s.split()[0:4]
        args = [float(x) for x in args]
        inks[index+1] = args

    return inks


def test():
    f = '000_TEST_Dom_Leonov.pdf', '000_TEST_Pla_Leonov.pdf', '000_TEST_Spe_Leonov.pdf', '0540_1.pdf', \
        '0540_2.pdf', 'test_manypages.pdf', 'test_cyan_50perc_Admin.pdf', 'HD_2pages_CM+CPant_Admin.pdf' #, '0045_Ivanovka_Kniga_Leonov_Inner.pdf'

    for pdf in f:
        pdf = 'test_pdf/' + pdf
        print pdf
        ink = analyze_inkcoverage(pdf)

        # Выводим результат (словарь)
        print ink

        # Разбираем словарь
        for page_number, ink_list in ink.iteritems():
            print 'Page', page_number, ':  ', "C {:.2f} M {:.2f} Y {:.2f} B {:.2f}".format(ink_list[0], ink_list[1], ink_list[2], ink_list[3])

        print '\n'

if __name__ == '__main__':
    test()