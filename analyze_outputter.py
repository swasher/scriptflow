# coding: utf-8
__author__ = 'swasher'

import os
import classes
import logging
import shutil

from os.path import join

def detect_outputter(pdfname):
    """
    Возвращает объект, соответствующий подрядчику вывода форм.
    :param pdfname: имя pdf файла
    :return: outputter (instance of FTP_server)
    """
    fname, fext = os.path.splitext(pdfname)
    parts = fname.split("_")

    # THIS CODE DEPRECATED AND REPLACED WITH ITERATED ON _DIC
    # if 'Leonov' in parts:
    # parts.remove('Leonov')
    #     outputter = Leonov
    # elif 'Korol' in parts:
    #     parts.remove('Korol')
    #     outputter = Korol
    # elif 'Admin' in parts:
    #     parts.remove('Admin')
    #     outputter = Admin
    # else:
    #     logging.error('{0} Outputter is UNKNOWN'.format(pdfname))
    #     exit()

    for company in classes.FTP_server._dic.keys():
        if company in parts:
            outputter = classes.FTP_server._dic[company]

    if 'outputter' in locals():
        print 'Outputter successfully detected: {}'.format(outputter.name)
    else:
        print 'Outputter cant detected'
        logging.error('{0} Outputter is UNKNOWN'.format(pdfname))
        exit()

    return outputter


def remove_outputter_title(pdfname):
    """
    Функция убирает подрядчика из имени файла (0537_Technoyug_Flier_Leonov.pdf -> 0537_Technoyug_Flier.pdf),
    затем переименовывает сам файл, и возвращает:
    :param pdfname: абсолютный путь к файлу
    :return: pdfname(string) абсолютный путь к переименованному файлу
    """

    fpath, (fname, fext) = os.path.dirname(pdfname), os.path.splitext(os.path.basename(pdfname))

    parts = fname.split("_")

    for company in classes.FTP_server._dic.keys():
        if company in parts:
            parts.remove(company)

    newname = join(fpath, '_'.join(parts)) + fext

    # Если подрядчик не определен, то файл не переименовывается и не перемещается
    #Для этой проверки сравнивается старое название с новым
    if pdfname != newname:
        shutil.move(pdfname, newname)

    return newname


def detect_preview_ftp(machine):
    """
    Возвращает объект, на какой фтп заливать превью. Связь между печатной машиной и фтп
    описана в поле uploadtarget класса PrintingPress
    :param pdfname:
    :return:
    """
    if machine.uploadtarget == '':
        preview_ftp = None
    else:
        preview_ftp = classes.FTP_server._dic[machine.uploadtarget]
    return preview_ftp
