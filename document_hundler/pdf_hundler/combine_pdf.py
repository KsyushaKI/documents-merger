import os
import shutil
import json
from PyPDF2 import PdfMerger
import zipfile


input_dir = 'document_hundler/pdf_hundler/input_files'
output_dir = 'document_hundler/pdf_hundler/output_files'
output_zip_file = 'document_hundler/pdf_hundler/output_zip/merged_pdf_with_jsone_data.zip'
result_pack_size = 100000


def combine_pdfs_and_make_json():
    pack_count = 1
    pack_size = 0
    pack_files = []
    pack_data = {}

    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            file_size = os.path.getsize(os.path.join(input_dir, filename))

            if pack_size + file_size > result_pack_size:
                pack_filename = 'pack_{}.pdf'.format(pack_count)
                merge_and_save_pdf(pack_files, pack_filename)
                pack_data[pack_filename] = pack_files
                pack_count += 1
                pack_size = 0
                pack_files = []

            pack_size += file_size
            pack_files.append(filename)

    if pack_files:
        pack_filename = 'pack_{}.pdf'.format(pack_count)
        merge_and_save_pdf(pack_files, pack_filename)
        pack_data[pack_filename] = pack_files

    save_dict_data_to_json(pack_data)
    result_to_zip()


def merge_and_save_pdf(file_list, pack_filename):
    pdf_merger = PdfMerger()

    for file in file_list:
        with open(os.path.join(input_dir, file), 'rb') as f:
            pdf_merger.append(f)

    with open(os.path.join(output_dir, pack_filename), 'wb') as f:
        pdf_merger.write(f)


def save_dict_data_to_json(dict_data):
    with open(os.path.join(output_dir, 'packs.json'), 'w') as f:
        json.dump(dict_data, f)


def result_to_zip():
    with zipfile.ZipFile(output_zip_file, 'w') as f:
        for file in os.listdir(output_dir):
            f.write(os.path.join(output_dir, file), arcname=file)


def clean_dir(dir):
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)


def clean_created_data():
    clean_dir(input_dir)
    clean_dir(output_dir)
