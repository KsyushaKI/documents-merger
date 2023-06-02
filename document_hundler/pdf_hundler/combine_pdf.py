import os
import shutil
import json
from PyPDF2 import PdfMerger
import zipfile


def combine_pdfs_and_make_json(
        input_dir,
        output_dir,
        output_zip_file,
        result_pack_size,
):
    pack_count = 1
    pack_size = 0
    pack_files = []
    pack_data = {}

    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            file_size = os.path.getsize(os.path.join(input_dir, filename))

            if pack_size + file_size > result_pack_size:
                pack_filename = 'pack_{}.pdf'.format(pack_count)
                merge_and_save_pdf(input_dir, output_dir, pack_files, pack_filename)
                pack_data[pack_filename] = pack_files
                pack_count += 1
                pack_size = 0
                pack_files = []

            pack_size += file_size
            pack_files.append(filename)

    if pack_files:
        pack_filename = 'pack_{}.pdf'.format(pack_count)
        merge_and_save_pdf(input_dir, output_dir, pack_files, pack_filename)
        pack_data[pack_filename] = pack_files

    save_dict_data_to_json(pack_data, output_dir)
    result_to_zip(output_zip_file, output_dir)


def merge_and_save_pdf(input_dir, output_dir, file_list, pack_filename):
    pdf_merger = PdfMerger()

    for file in file_list:
        with open(os.path.join(input_dir, file), 'rb') as f:
            pdf_merger.append(f)

    with open(os.path.join(output_dir, pack_filename), 'wb') as f:
        pdf_merger.write(f)


def save_dict_data_to_json(dict_data, output_dir):
    with open(os.path.join(output_dir, 'packs.json'), 'w') as f:
        json.dump(dict_data, f)


def result_to_zip(output_zip_file, output_dir):
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


def clean_created_data(*path_to_dirs):
    for dir in path_to_dirs:
        clean_dir(dir)
