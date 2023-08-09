from flask import flash


def validate(files, file_format):
    result = True
    for file in files:
        if not file.filename.endswith(file_format):
            flash(f'Файл {file.filename} не является {file_format}', 'danger')
            result = False

    if len(files) == 1:
        flash('Выбран только один файл для объединения', 'danger')
        result = False

    return result
