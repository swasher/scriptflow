#!/usr/bin/python
#coding: utf-8

__author__ = 'Алексей'
from subprocess import Popen, PIPE


def analyze_colorant(pdfname):
    """
    :param pdfname: path to pdf file
    :return:
    total_pages(int) - количество страниц
    total_plates(int) - общее количество плит
    pdf_colors(dict) - словарь, где ключ - номер страницы, значение - список сепараций
    """
    cmd = r"cat {} | grep --binary-files=text 'HDAG_ColorantNames'".format(pdfname)
    result_strings = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE).stdout.read().splitlines()

    total_plates = 0
    #total_pages = len(result_strings)
    pdf_colors = {}
    for index, color in enumerate(result_strings):
        # Убираем из строки HDAG_ColorantNames занки '/[]', разделяем
        # строку на список, убираем первый элемент (HDAG_ColorantNames)
        separations = color.translate(None, '/[]').split()[1:]
        total_plates += len(separations)

        #fix pantone names
        separations = [s.replace('#20', '_') for s in separations]

        #Создаем словарь, где ключ - номер страницы, значение - список сепараций
        pdf_colors[index+1] = separations
    return total_plates, pdf_colors


def test():
    f = ['test_pdf/000_TEST_Dom_Leonov.pdf',
         'test_pdf/000_TEST_Pla_Leonov.pdf',
         'test_pdf/000_TEST_Spe_Leonov.pdf',
         'test_pdf/0540_1.pdf',
         'test_pdf/0540_2.pdf',
         'test_pdf/0045_Ivanovka_Kniga_Leonov_Inner.pdf',
         'test_pdf/Multi-page-catalog-CMYK_1030x780_6p_Admin.pdf']
    #f = ['test_pdf/Multi-page-catalog-CMYK_1030x780_6p_Admin.pdf']

    for i in f:
        print '\n\n'
        total_plates, pdf_colors = analyze_colorant(i)
        print i
        print total_plates, pdf_colors, '\n'
        for page_number, ink_list in pdf_colors.iteritems():
            print page_number, ink_list


if __name__ == '__main__':
    test()
