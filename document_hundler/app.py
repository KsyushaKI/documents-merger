import os
from dotenv import load_dotenv
import document_hundler.excel_hundler.combine_excel as ce
import document_hundler.pdf_hundler.combine_pdf as cp
from document_hundler.save_and_validate import save, validate
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
            'Отсутствует столбец "Номер" или что-то пошло не так',
            'danger'
        )
        return redirect(url_for('get_excel_hundler'))

    return send_file(ce.path_to_output_file, as_attachment=True)


@app.get('/pdf_hundler')
def get_pdf_hundler():
    return render_template("pdf.html")


@app.post('/pdf_hundler/downland')
def get_merged_pdf():
    pdf_files = request.files.getlist('pdffile')
    save(pdf_files, cp.input_dir)

    try:
        cp.combine_pdfs_and_make_json()
    except:
        flash('Что-то пошло не так', 'danger')
        return redirect(url_for('get_pdf_hundler'))
    finally:
        cp.clean_created_data(cp.input_dir, cp.output_dir)

    return send_file(cp.output_zip_file, as_attachment=True)
