#!/usr/bin/python
#coding: utf-8

######## TO-DO###############################
#TODO сделать логирование, чтобы смотреть не дошедшие до финиша заливки
#TODO оповещение смс
#TODO превьюхи
#TODO ink cov
#TODO кнопка run
#TODO перевод на django
#TODO заменить тело на функцию main
#TODO переименовать flow в main
####

################ IMPORT SECTION ######################

import os
import sys
import shutil
import datetime
import socket
import logging
import tempfile

from os.path import dirname, splitext
from subprocess import Popen, PIPE

#import classes

from util import dict_to_multiline, error_text, crop
from sendfile import sendfile
from analyze_common import analyze
from analyze_colorant import analyze_colorant
from analyze_papersize import analyze_papersize
from analyze_outputter import detect_outputter, detect_preview_ftp, remove_outputter_title
from analyze_inkcoverage import analyze_inkcoverage

################ INITIALIZING SECTION ######################

#script home
homedir = os.path.abspath(os.path.dirname(sys.argv[0])) + '/'

#incrond watched this dir (must be with trail slash)
inputdir = homedir + 'input/'

#куда писать вывод на сайт
phpfile = homedir + 'web/data.php'


######## some setups #################
pdfname = sys.argv[1]
html_data = {}

socket.setdefaulttimeout(10.0)

logging.basicConfig(format='%(asctime)s %(levelname)s \t %(message)s<p>',
                    datefmt='%d/%m/%Y %H:%M', filename=homedir+'web/flow.html', level=logging.DEBUG)

# logger = logging.getLogger("my logger")
# logger.setLevel(logging.DEBUG)
# # Format for our loglines
# formatter = logging.Formatter("%(asctime)s %(levelname)s \t %(message)s")
# # Setup console logging
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# ch.setFormatter(formatter)
# logger.addHandler(ch)
# # Setup file logging as well
# fh = logging.FileHandler('flow.log')
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(formatter)
# logger.addHandler(fh)

######### end section ################


######### function declaration ######
def siteecho(html_data):
    """
    Сначала к строке добавляем файл, получается, что новая строка в начале файла.
    Потом все записываем обратно в файл.
    """
    html = """<tr class={bg}> \
<td>{dt}</td> \
<td>{pdfname}</td> \
<td>{machine}</td> \
<td>{total_pages} компл.</td> \
<td><span data-toggle="tooltip" data-placement="right" title="{colors}">
        <button type="button" class="btn btn-default btn-xs">{total_plates} плит</button>
    </span>
</td> \
<td>{dest}</td> \
<td>{output}</td> \
<td>{preview}</td> \
</tr>\n"""
    message = html.format(**html_data)

    with open(phpfile, 'r') as f:
        data = f.read()
        outdata = message+data

    with open(phpfile, 'w') as f:
        f.write(outdata)

######### end function declaration ######



###########################################################
### ТУТ НАЧИНАЕТСЯ ВЫПОЛНЕНИЕ СКРИПТА
############################################################

print '\n\n'
print 'START PROCESSING {}'.format(pdfname)
print '----------------------------------------------------------------'


#Move pdf to temp
#-----------------------------------------------------------------
try:
    tempdir = tempfile.mkdtemp(dir=homedir)+'/'
    shutil.move(inputdir+pdfname, tempdir+pdfname)
    pdf_abs_path = tempdir+pdfname
except Exception, e:
    logging.error('{0}: Cant move to temp: {1}'.format(pdfname, e))
    os.unlink(pdf_abs_path)
    exit()


#Check if file is PDF
#--------------------
pdfcheck_command = "file {} | tr -s ':' | cut -f 2 -d ':'".format(pdf_abs_path)
result_strings = Popen(pdfcheck_command, shell=True, stdin=PIPE, stdout=PIPE).stdout.read().split(',')[0].strip()
file_is_not_pdf_document = result_strings != 'PDF document'

pdfExtension = splitext(pdf_abs_path)[1]
if pdfExtension != ".pdf" or file_is_not_pdf_document:
    logging.error('{0} File is NOT PDF - exiting...'.format(pdfname))
    os.unlink(pdf_abs_path)
    os.removedirs(tempdir)
    exit()

#Check if file created with Signa
#--------------------------------
pdfinfo_command = "pdfinfo {} | grep Creator | tr -s ' ' | cut -f 2 -d ' '".format(pdf_abs_path)
result_strings = Popen(pdfinfo_command, shell=True, stdin=PIPE, stdout=PIPE).stdout.read().strip()
if result_strings == 'PrinectSignaStation':
    print '{} is valid PrinectSignaStation file.'.format(pdfname)
else:
    logging.warning('{} created with {}, not Signastation!'.format(pdfname, result_strings))
    #TODO продумать, что делать, если файл не сигновский


#Detect properties
##----------------------------------------------------------------
# machine: plate for machine, it's an INSTANCE of PrintingPress class (AD, SM or PL)
# plates: number of plates
# outputter: Кто выводит - leonov, korol, etc. - это объект типа FTP_server
# total_pages, total_plates, pdf_colors - страниц, плит, текстовый блок о красочности

machine, complects = analyze(pdf_abs_path)

if machine is None:
    logging.error('Cant detect machine for {}'.format(pdfname))
    print 'Cant detect machine for {}'.format(pdfname)
    print 'Exiting...'
    os.unlink(pdf_abs_path)
    os.removedirs(tempdir)
    exit()

# total_pages тут определяется по кол-ву строк, содержащих тэг HDAG_ColorantNames
total_plates, pdf_colors = analyze_colorant(pdf_abs_path)

paper_size = analyze_papersize(pdf_abs_path)

outputter_ftp = detect_outputter(pdfname)



preview_ftp = detect_preview_ftp(machine)

# Переименовываем - из названия PDF удаляется имя выводильщика.
pdf_abs_path = remove_outputter_title(pdf_abs_path)

pdfPath, (pdfName, pdfExtension) = dirname(pdf_abs_path), splitext(os.path.basename(pdf_abs_path))


# Проверка, соответствует ли PDF известному формату пластины
##----------------------------------------------------------------
# TODO Проверка, соответствует ли PDF известному формату пластины



# Compress via gs and crop via perl script.
# preview_abs_path has a full path to compressed and cropped pdf
#----------------------------------------------------------------

previewname = pdfName + '.' + outputter_ftp.name + pdfExtension
previewtempname = tempdir + pdfName + '.' + outputter_ftp.name + '.temp' + pdfExtension
preview_abs_path = tempdir + pdfName + '.' + outputter_ftp.name + pdfExtension

crop(pdf_abs_path, previewtempname)

gs_compress = "gs -q -sDEVICE=pdfwrite -dDownsampleColorImages=true " \
              "-dColorImageResolution=120 -dCompatibilityLevel=1.4 "\
              "-dNOPAUSE -dBATCH -sOutputFile={output} {input}"\
              .format(input=previewtempname, output=preview_abs_path)
os.system(gs_compress)

os.unlink(previewtempname)


### CUSTOM OPERATION DEPENDS ON OUTPUTTER
#----------------------------------------
if outputter_ftp.name == 'Leonov':
    if machine.name == 'Speedmaster':
        outputter_ftp.todir = '_1030x770'
    elif machine.name == 'Planeta':
        outputter_ftp.todir = '_1010x820'
    elif machine.name == 'Adast':
        outputter_ftp.todir = '_ADAST'
    else:
        outputter_ftp.todir = ''

if outputter_ftp.name == 'Korol':
    # may be rotate90?
    ###add label 'paper width' for korol
    fname, fext = os.path.splitext(pdfname)
    if machine.name == 'SM':
        newname = fname + '_' + str(SM.plate_w) + fext
    elif machine.name == 'PL':
        newname = fname + '_' + str(PL.plate_w) + fext
    elif machine.name == 'AD':
        newname = fname + '_' + str(AD.plate_w) + fext
    else:
        pass  #что делать, если машина не определилась???
    shutil.move(tempdir + pdfname, tempdir + newname)
    pdfname = newname
    pdf_abs_path = tempdir + newname


#Send Preview PDF to printing press FTP
#-------------------------------------------------------
if os.path.isfile(preview_abs_path):
    if preview_ftp:
        status_kinap, e_kinap = sendfile(preview_abs_path, preview_ftp)
    else:
        status_kinap, e_kinap = False, "Machine can't be detected or don't have ftp"
else:
    print 'Preview not found and not upload'
    status_kinap, e_kinap = False, 'Preview not found'


#Send Original PDF to Outputter
#---------------------------------------------------------
status_outputter, e_outputter = sendfile(pdf_abs_path, outputter_ftp)


#Словарь html_data подставляется в шаблон для формирования web-страницы
# dt (Текущая дата и время), pdfname, machine,
# complects, total_plates, dest, send-output success, send preview sucess, colors
text_outputter = error_text(status_outputter, e_outputter)
text_kinap = error_text(status_kinap, e_kinap)
if not status_outputter:
    bg = 'danger'
elif not status_kinap:
    bg = 'warning'
else:
    bg = 'default'

html_data['dt'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
html_data['pdfname'] = pdfname
html_data['machine'] = machine.name
html_data['total_pages'] = complects
html_data['total_plates'] = total_plates
html_data['dest'] = outputter_ftp.name
html_data['output'] = text_outputter
html_data['preview'] = text_kinap
html_data['colors'] = dict_to_multiline(pdf_colors)
html_data['bg'] = bg

siteecho(html_data)

try:
    os.unlink(pdf_abs_path)
    os.unlink(preview_abs_path)
    os.removedirs(tempdir)
    print '\nSUCCESSFULLY finish and clean.'
except Exception, e:
    print 'Problem with cleaning:', e

