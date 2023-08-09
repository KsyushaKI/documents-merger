import os
from PyPDF2 import PdfMerger


path_to_output_file = (f'{os.getcwd()}/'
                       f'documents_merger/pdf_merger/output_files/merged.pdf')


def merge_and_save_pdf(pdf_files):
    merger = PdfMerger()

    for file in pdf_files:
        merger.append(file)

    merger.write(path_to_output_file)
    merger.close()