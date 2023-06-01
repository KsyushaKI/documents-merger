import pandas as pd
import os


value_for_sort = 'Номер'
excel_file_column_name = 'File_Name'
path_to_save = 'document_hundler/excel_hundler/output_file'
merged_file_name = 'merged_file.xlsx'


def merge_and_save_excels(xl_files):
    all_sheet_names = []
    combined = pd.DataFrame()

    for xl_file in xl_files:
        xl_file_obj = pd.ExcelFile(xl_file)

        for sheet_name in xl_file_obj.sheet_names:
            all_sheet_names.append(sheet_name)
            data = pd.read_excel(xl_file_obj, sheet_name=sheet_name)
            data.insert(0, excel_file_column_name, xl_file.filename)
            combined = pd.concat([combined, data]).sort_values([value_for_sort])

    combined.to_excel(
        os.path.join(path_to_save, merged_file_name),
        sheet_name=all_sheet_names[0],
        index=False
    )
