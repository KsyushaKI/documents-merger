import pandas as pd
import os


path_to_output_file = f'{os.getcwd()}/documents_merger/excel_merger/merged.xlsx'


def merge_and_save_excels(xl_files):
    file_name_column = 'original_file_name'
    merger = pd.DataFrame()

    for xl_file in xl_files:
        xl_file_obj = pd.ExcelFile(xl_file)

        for sheet_name in xl_file_obj.sheet_names:
            data = pd.read_excel(xl_file_obj, sheet_name=sheet_name)
            data.insert(0, file_name_column, xl_file.filename)
            merger = pd.concat([merger, data])

    merger.to_excel(path_to_output_file, index=False)
