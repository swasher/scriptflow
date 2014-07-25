#!/usr/bin/python
#coding: utf-8
__author__ = 'Алексей'


class FTP_server(object):
    """
    _registry - Это список объектов

    for item in writer._registry:
        print 'name=', item.name, 'ip=', item.ip

    _dic - это словарь, где ключем является имя (string) объекта, а значением - сам объект.

    current_instance = FTP_server._dic['SM']
    >>>print FTP_server._dic.keys()
    >>>['Adast', 'Speedmaster', 'Leonov', 'Korol', 'Admin']
    """
    _registry = []
    _dic = {}

    def __init__(self, name, ip, port, login, passw, todir):
        self._registry.append(self)
        self._dic[name] = self
        self.name = name
        self.ip = ip
        self.port = int(port)
        self.login = login
        self.passw = passw
        self.todir = todir


""" Initializing FTP_server instances
`contractors` file describe ftp's parameters (both for contractors and previews)
format:
<name> <ip> <login> <password> <todir>
Fields separated with space, and '' for empty todir
"""
with open('contractors') as contractors:
    for contractor in contractors:
        name, ip, port, login, passw, todir = contractor.split(' ')
        todir = todir.rstrip()

        if todir == "\'\'":
            todir = ''

        dummy = FTP_server(name, ip, port, login, passw, todir)

        #Change instance name from 'dummy' to 'Speedmaster', 'Korol' etc.
        globals()[name] = globals()['dummy']
        del globals()['dummy']


class PrintingPress():
    """
    Класс описывает печатные машины. Итерировать можно аналогично FTP_server.
    uploadtarget - должно соотв. имени инстанса Write, куда производить заливку на фтп.
    """
    _registry = []
    _dic = {}

    def __init__(self, name, uploadtarget, plate_w, plate_h, klapan):
        self._registry.append(self)
        self._dic[name] = self
        self.name = name
        self.uploadtarget = uploadtarget
        self.plate_w = plate_w
        self.plate_h = plate_h
        self.klapan = klapan


""" Initializing PrintingPress instances
`printingmachines` file describe printing machines parameters
format:
<Name> <Uploadtarget> <Plate width> <Plate height> <Klapan gap>
Uploadtarget must correspond to appropriate FTP_server.name, or '' for absent uploadtarget
Fields separated with space
"""
with open('printingmachines') as printingmachines:
    for machine in printingmachines:
        name, uploadtarget, plate_w, plate_h, klapan = machine.split(' ')
        uploadtarget = uploadtarget.rstrip()

        if uploadtarget == "\'\'":
            uploadtarget = None

        dummy = PrintingPress(name, uploadtarget, int(plate_w), int(plate_h), int(klapan))

        #Change instance name from 'dummy' to 'Speedmaster', 'Korol' etc.
        globals()[name] = globals()['dummy']
        del globals()['dummy']

# DEPRECATED CODE BLOCK
#AD = PrintingPress('Dominant', 'AD_ftp', 740, 575, 25)
#SM = PrintingPress('Speedmaster', 'SM_ftp', 1030, 770, 40)
#PL = PrintingPress('Planeta', '', 1010, 820, 55)


def test():
    #for x in PrintingPress._registry:
    #    print x
    #print PrintingPress._registry
    #
    # for x, y in PrintingPress._dic.items():
    #    print x

    #print PrintingPress._dic.keys()

    for x in PrintingPress._registry:
        print 'name =', x.name
        print 'uploadtarget =', x.uploadtarget
        print 'plate_w =', x.plate_w
        print 'plate_h =', x.plate_h
        print 'klapan =', x.klapan


if __name__ == '__main__':
    test()
