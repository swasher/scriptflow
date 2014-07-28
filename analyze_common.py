#!/usr/bin/python
#coding: utf-8
__author__ = 'Алексей'

from subprocess import Popen, PIPE
from util import mm, pt

# see description at flow.py
#from classes import PrintingPress
#__import__('classes', fromlist=PrintingPress._dic.keys())

#from classes import AD, SM, PL
import classes

def analyze(pdfname):
    """
    Функция определяет основные параметры PDF (основываясь на первой странице файла)
    :param
        pdfname: str
         Путь к pdf файлу
    :return:
        machine - объект типа PrintingPress (or None if cant detect)
        pages - кол-во страниц
    """

    pdfinfo_command = r"pdfinfo -box {0} | grep 'Page'".format(pdfname)
    pdfinfo_result = Popen(pdfinfo_command, shell=True, stdin=PIPE, stdout=PIPE).stdout.read().splitlines()

    pages = pdfinfo_result[0].split(" ")[10]

    s = pdfinfo_result[1].split(" ")
    width = s[7]
    height = s[9]
    width = mm(width)
    height = mm(height)

    # if widthmm == 740:
    #     machine = AD
    # elif widthmm == 1010:
    #     machine = PL
    # elif widthmm == 1030:
    #     machine = SM
    # else:
    #     machine = 'UNKNOWN'

    # Итерируем по всем инстансам класса PrintingPress, если у очередного объекта
    # совпадают ширина и высота пластины с шириной и высотой первого листа pdf,
    # тогда копируем этот инстанс в переменную machine
    machine = None
    for press in classes.PrintingPress._registry:
        if width == press.plate_w and height == press.plate_h:
            machine = classes.PrintingPress._dic[press.name]

    return machine, pages


def test():
    pass

if __name__ == '__main__':
    test()