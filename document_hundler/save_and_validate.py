from werkzeug.utils import secure_filename
from flask import flash
import os


def save(files, path_to_save):
    for file in files:
        file_name = secure_filename(file.filename)
        file.save(os.path.join(path_to_save, file_name))


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
