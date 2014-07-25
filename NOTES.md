Софт для обрабоки изображений

- ghostscript

Основная программа для работы с ps, eps, pdf. Может практически все.

- icepdf 

Профессиональный платный софт, есть опенсорс версия

- pdfbox

опенсорс ява библиотека для PDF. Может в командной строке применяться https://pdfbox.apache.org/commandline/

- inkscape

Программа типа корел, может работать из командной строки
Применение - преобразование форматов, конвертация, работает с векторным svg. http://inkscape.org/doc/inkscape-man.html

- PyPDF2

питоновская библиотека для PDF, - в основном для работы со страницами.  Объеденяет, разъеденяет, поворачивает, etc.

- stapler 

дохлая питоновская либа - объеденение пдф-ов

- pdftk

* Merge PDF Documents or Collate PDF Page Scans
       * Split PDF Pages into a New Document
       * Rotate PDF Documents or Pages
       * Decrypt Input as Necessary (Password Required)
       * Encrypt Output as Desired
       * Fill PDF Forms with X/FDF Data and/or Flatten Forms
       * Generate FDF Data Stencils from PDF Forms
       * Apply a Background Watermark or a Foreground Stamp
       * Report PDF Metrics, Bookmarks and Metadata
       * Add/Update PDF Bookmarks or Metadata
       * Attach Files to PDF Pages or the PDF Document
       * Unpack PDF Attachments
       * Burst a PDF Document into Single Pages
       * Uncompress and Re-Compress Page Streams
       * Repair Corrupted PDF (Where Possible)
       
- PDFMiner
       
Unlike other PDF-related tools, it focuses entirely on getting and analyzing text data. 
Умеет работать (в т.ч. добавлять) с объектами внутри PDF-а

Имеет утилиты pdf2txt.py (extracts text contents from a PDF file), dumppdf.py (dumps the internal contents of a PDF file in pseudo-XML format)

- Утилита для кропа pdf

    perl_command = "perl pdfcrop.pl {input} {output}".format(input=previewtempname, output=preview_abs_path)
    os.system(perl_command)