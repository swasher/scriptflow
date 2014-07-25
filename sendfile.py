#!/usr/bin/python
#coding: utf-8
__author__ = 'Алексей'

from ftplib import FTP
import sys
import os
import logging
import time


def handle(block):
    global sizeWritten, totalSize
    sizeWritten += 1024
    percentComplete = sizeWritten*100 / totalSize
    sys.stdout.write("{0} percent complete \r".format(percentComplete))


def sendfile(pdf_ads_path, receiver):
    """
    Функция выполняет заливку на фтп
    :param pdfname:str Путь к файлу (абсолютный)
    :param receiver:str Объект получателя, список получателей в файле ftps, объекты фрмируются из файла функцией -==-
    :return: status:boolean - флаг удачного завершения
                e:exception - код ошибки
    """
    global sizeWritten, totalSize
    logger = logging.getLogger("my logger")

    status = True
    e = None

    pdfname = os.path.basename(pdf_ads_path)

    sizeWritten = 0
    totalSize = os.path.getsize(pdf_ads_path)
    #print 'name:',receiver.name
    #print 'ip:',receiver.ip
    #print 'port:',receiver.port,  type(receiver.port)
    #print 'login:',receiver.login
    #print 'pass:',receiver.passw
    print '\nTry connect to {0}...'.format(receiver.name)
    try:
        ftp = FTP()
        ftp.connect(receiver.ip, port=receiver.port, timeout=20)   # timeout is 15 seconds
        ftp.login(receiver.login, receiver.passw)
    except Exception, e:
        logging.error('{0}:{1}: {2}'.format(pdfname, receiver.name, e))
        print '==>connect FAILED with error: {0}'.format(e)
        status = False
        return status, e
    else:
        print '==>connect passed'
        localfile = open(pdf_ads_path, "rb")
        try:
            ftp.set_pasv(True)
            ftp.cwd(receiver.todir)
            print 'Start uploading ', pdfname, ' to ', receiver.name, '...'
            start = time.time()
            ftp.storbinary("STOR " + pdfname, localfile, 1024, handle)
            #print 'Size in kb ', totalSize/1024
            #print 'Time in s ', (time.time()-start)
            speed = totalSize/(time.time()-start)/1024
            print 'Speed: {0:.1f} kB/s equivalent to {1:.2f} MBit/s'.format(speed, speed*8/1024)
        except Exception, e:
            logging.error('{0}:{1}: {2}'.format(pdfname, receiver.name, e))
            print 'upload FAILED with error: {0}'.format(e)
            status = False
            return status, e
            #siteecho(pdfname, receiver.name, 'FAILED', machine, complects, html_data)
        else:
            logging.info('{0}:{1}: upload OK'.format(pdfname, receiver.name))
            print 'Upload finished OK'
            #siteecho(pdfname, receiver.name, 'Upload OK', machine, complects, html_data)
        finally:
            localfile.close()
    finally:
        ftp.close()

    return status, e


def test():
    pass


if __name__ == '__main__':
    test()
