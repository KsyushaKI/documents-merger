import os
from dotenv import load_dotenv
import document_hundler.excel_hundler.combine_excel as ce
import document_hundler.pdf_hundler.combine_pdf as cp
from document_hundler.save_and_validate import save, validate
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    flash,
    render_template,
    request,
    redirect,
    url_for,
    send_file,
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

current_dir = os.getcwd()
pdf_input_dir = f'{current_dir}/document_hundler/pdf_hundler/input_files'
pdf_output_dir = f'{current_dir}/document_hundler/pdf_hundler/output_files'
pdf_output_zip_file = f'{current_dir}/document_hundler/pdf_hundler/output_zip/merged_pdf_with_jsone_data.zip'
path_to_excel_result = f'{current_dir}/document_hundler/excel_hundler/output_file/merged_file.xlsx'
path_to_pdf_result = f'{current_dir}/document_hundler/pdf_hundler/output_zip/merged_pdf_with_jsone_data.zip'
path_to_save_pdf = f'{current_dir}/document_hundler/pdf_hundler/input_files'
pdf_result_pack_size = 100000


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return render_template("index.html")


@app.get('/excel_hundler')
def get_excel_hundler():
    return render_template("excel.html")


@app.post('/excel_hundler/downland')
def get_merget_excel():
    xl_files = request.files.getlist('excelfile')

    if not validate(xl_files, '.xlsx'):
        return redirect(url_for('get_excel_hundler'))

    try:
        ce.merge_and_save_excels(xl_files)
    except:
        flash(
            'Вероятно отсутствует столбец "Номер"',
            'danger'
        )
        return redirect(url_for('get_excel_hundler'))

    return send_file(path_to_excel_result, as_attachment=True)


@app.get('/pdf_hundler')
def get_pdf_hundler():
    return render_template("pdf.html")


@app.post('/pdf_hundler/downland')
def get_merged_pdf():
    pdf_files = request.files.getlist('pdffile')

    if not validate(pdf_files, '.pdf'):
        return redirect(url_for('get_pdf_hundler'))

    for file in pdf_files:
        file_name = secure_filename(file.filename)
        app.config['UPLOAD_FOLDER'] = path_to_save_pdf
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

    cp.combine_pdfs_and_make_json(
        pdf_input_dir,
        pdf_output_dir,
        pdf_output_zip_file,
        pdf_result_pack_size
    )

    cp.clean_created_data(pdf_input_dir, pdf_output_dir)

    return send_file(path_to_pdf_result, as_attachment=True)
