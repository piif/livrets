#!/usr/bin/env python3

from pypdf import PdfReader, PdfWriter, Transformation, PageObject
import sys, getopt

def Usage(message=None):
    if message is not None:
        print(f'    {message}', file=sys.stderr)
    print(f"""    Usage : {argv0} -i in_file -o out_file [ -l | -s ] [ -n N ]
      reorder pages to booklets
      -i : input pdf file path
      -o : output pdf file path
      -l : prepare for long border recto-verso printing (default)
      -s : prepare for short border recto-verso printing
      -n N : prepare for N sheets booklets (thus N*4 pages per sheet), 0=one global book (default)
    """, file=sys.stderr)
    sys.exit(1)



def outputSheet(pdf_reader, pdf_writer, border, p0, p1, p2, p3):
    print("generating sheet with pages", p0, p1, p2, p3)
    global h, w, scale, scale_translate, allPages

    out = PageObject.create_blank_page(width = h, height = w)

    if p0 < allPages:
        page0 = pdf_reader.pages[p0]
        page0.add_transformation(scale)
        out.merge_page(page0)

    if p1 < allPages:
        out1 = PageObject.create_blank_page(width = h, height = w)
        page1 = pdf_reader.pages[p1]
        out1.merge_page(page1)
        out1.add_transformation(scale_translate)
        out.merge_page(out1)

    pdf_writer.add_page(out)
    # # pdf_writer.add_page(page1)


    out = PageObject.create_blank_page(width = h, height = w)

    if p2 < allPages:
        page2 = pdf_reader.pages[p2]
        op = Transformation().rotate(180).translate(w, h).scale(0.7, 0.7)
        page2.add_transformation(scale)
        out.merge_page(page2)

    if p3 < allPages:
        out1 = PageObject.create_blank_page(width = h, height = w)
        page3 = pdf_reader.pages[p3]
        out1.merge_page(page3)
        out1.add_transformation(scale_translate)
        out.merge_page(out1)
        if border == 'long':
            out.rotate(180)

    pdf_writer.add_page(out)


def convert(in_path, out_path, border, sheets):
    global h, w, scale, scale_translate, allPages

    try:
        pdf_reader = PdfReader(in_path)
    except Exception as err:
        Usage(f"Can't open input file : {err}")

    pdf_writer = PdfWriter()

    page0 = pdf_reader.pages[0]
    h = int(page0.mediabox.top)
    w = int(page0.mediabox.right)
    t = int(0.5*float(h))
    scale = Transformation().scale(sx=0.7, sy=0.7)
    scale_translate = scale.translate(t, 0.0)

    allPages = len(pdf_reader.pages)
    if sheets == 0:
        sheets = (allPages + 3) // 4
    pagesPerBooklet = sheets*4
    booklet = 0
    while booklet * pagesPerBooklet < allPages:
        pageFrom = booklet * pagesPerBooklet
        pageTo = (booklet+1) * pagesPerBooklet - 1
        while pageFrom < pageTo:
            outputSheet(pdf_reader, pdf_writer, border, pageFrom+1, pageTo-1, pageTo, pageFrom)
            pageFrom += 2
            pageTo -= 2
        booklet += 1

    # print(f'h={h}, w={w}, t={t}')

    try:
        with open(out_path, 'wb') as out_file:
            pdf_writer.write(out_file)
    except Exception as err:
        Usage("Can't open output file")


def parseArgs(argv):
    try:
        optlist, args = getopt.getopt(argv, 'i:o:lsn:', [ 'input=', 'output=', 'long', 'short', 'sheets='] )
    except getopt.GetoptError as err:
        Usage(err)

    if len(args)!=0:
        Usage("Too many arguments")

    in_path = None
    out_path = None
    border = 'long'
    sheets = 0
    for o, a in optlist:
        if o in ('-i', '--input'):
            in_path = a
        elif o in ('-o', '--output'):
            out_path = a
        elif o in ('-l', '--long'):
            border = 'long'
        elif o in ('-s', '--short'):
            border = 'short'
        elif o in ('-n', '--sheets'):
            try:
                sheets = int(a)
            except ValueError:
                Usage("-n / --sheets requires a number as argument")
        else:
            Usage("unhandled option")

    return in_path, out_path, border, sheets


def main(argv):
    in_path, out_path, border, sheets = parseArgs(argv)
    if in_path is None or out_path is None:
        Usage("Both input and output pathes are required")

    convert(in_path, out_path, border, sheets)

argv0=sys.argv[0]
if __name__ == '__main__':
    main(sys.argv[1:])