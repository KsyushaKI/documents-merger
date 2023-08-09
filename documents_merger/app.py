import os
from dotenv import load_dotenv
import documents_merger.excel_merger.combine_excel as ce
import documents_merger.pdf_merger.combine_pdf as cp
from documents_merger.validate import validate
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
def get_merged_excel():
    xl_files = request.files.getlist('excelfile')

    if not validate(xl_files, '.xlsx'):
        return redirect(url_for('get_excel_hundler'))

    try:
        ce.merge_and_save_excels(xl_files)
        return send_file(ce.path_to_output_file, as_attachment=True)
    except Exception:
        flash('Что-то пошло не так', 'danger')
        return redirect(url_for('get_excel_hundler'))


@app.get('/pdf_hundler')
def get_pdf_hundler():
    return render_template("pdf.html")


@app.post('/pdf_hundler/downland')
def get_merged_pdf():
    pdf_files = request.files.getlist('pdffile')

    if not validate(pdf_files, '.pdf'):
        return redirect(url_for('get_pdf_hundler'))

    try:
        cp.merge_and_save_pdf(pdf_files)
        return send_file(cp.path_to_output_file, as_attachment=True)
    except Exception:
        flash('Что-то пошло не так', 'danger')
        return redirect(url_for('get_pdf_hundler'))
