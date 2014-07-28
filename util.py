#!/usr/bin/python
#coding: utf-8
# __author__ = 'Алексей'

from analyze_papersize import analyze_papersize
from PyPDF2.pdf import PdfFileWriter, PdfFileReader
from analyze_papersize import analyze_papersize
#from classes import AD, SM, PL
from classes import PrintingPress
import os


def mm(points):
    """
    Convert postscript points to millimetres. 1 pt = 25.4/72 mm
    :param points: (float) points
    :return: (float) millimetres
    """
    return int(round(float(points)/72*25.4))


def pt(mm):
    """
    :param mm: (float)
    :return: points (float)
    """
    return int(float(mm)*72/25.4)



def dict_to_multiline(dic):
    """
    Функция преобразует словарь в текстовый объект, где каждая строка вида key: value1 value.
    Используется, например, для вывода колоранотов в html
    :param dic(dic): словарь
    :return: text(str)
    """
    text = ''
    for k, v in dic.iteritems():
        text += str(k)+': '
        for i in v:
            text += i + ' '
        text += "\n"
    return text


def error_text(status, e):
    if status:
        text = "OK"
    else:
        if e:
            text = e
        else:
            text = "Unknown error"
    return text

def crop(pdf_in, pdf_out):
    """
    Параметры
    pdf_in - абсолютный путь к пдф
    pdf_out - абсолютный путь для исходящего пдф
    :return: status
    """

    """ Временно к функции добавлен второй параметр - pdf_out. В продакшн она должна сохранять результат кропа
     в тот же файл
    """
    status = True

    # Словарь с размерами бумаги для каждой страницы
    papers = analyze_papersize(pdf_in)  # like {1: ('Speedmaster', 900, 640), 2: ('Dominant', 640, 450)}

    # TODO Доработать временное решение кропа в отсутствии инфы о размере бумаги.
    if papers == {}:
        perl_crop = "perl pdfcrop.pl {} {}".format(pdf_in, pdf_out)
        os.system(perl_crop)
        return status

    input = PdfFileReader(file(pdf_in, "rb"))
    output = PdfFileWriter()

    # Количество страниц
    pages_qty = input.getNumPages()

    for index in range(pages_qty):
        paper_machine = papers[index+1][0]
        paper_w = papers[index+1][1]
        paper_h = papers[index+1][2]

        for m in PrintingPress._registry:
            if paper_machine == m.name:
                machine = m

        plate_w = machine.plate_w
        plate_h = machine.plate_h

        page = input.getPage(index)

        """ EXAMLE
        # The resulting document has a trim box that is 200x200 points
        # and starts at 25,25 points inside the media box.
        # The crop box is 25 points inside the trim box.
        print mm(page.mediaBox.getUpperRight_x()), mm(page.mediaBox.getUpperRight_y())
        page.trimBox.lowerLeft = (25, 25)
        page.trimBox.upperRight = (225, 225)
        page.cropBox.lowerLeft = (50, 50)
        page.cropBox.upperRight = (200, 200)
        """

        print 'Crop page {} to paper {}x{}'.format(index+1, paper_w, paper_h)
        page.mediaBox.lowerLeft = ((pt(plate_w - paper_w)/2), pt(machine.klapan))  # отступ слева, отступ снизу
        page.mediaBox.upperRight = (pt(paper_w + (plate_w - paper_w)/2), pt(paper_h + machine.klapan))  # ширина+отступ, высота+отступ

        output.addPage(page)

    outputstream = file(pdf_out, "wb")
    output.write(outputstream)
    outputstream.close()

    return status


def test():
    pdffile_in = r'test_pdf/0384_Repro_Arma_Leonov.pdf'
    pdffile_out = r'test_pdf/output.pdf'
    crop(pdffile_in, pdffile_out)


if __name__ == '__main__':
    test()
