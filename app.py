from flask import Flask, render_template, request, send_file, session, redirect, url_for, flash
import fitz  # type: ignore # PyMuPDF
import os
import uuid
from rembg import remove # type: ignore
from PIL import Image

app = Flask(__name__)
app.secret_key = 'ganti_secret_key_anda'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def unique_filename(ext):
    return f"{uuid.uuid4().hex}.{ext}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['GET', 'POST'])
def compress_pdf():
    if request.method == 'POST':
        file = request.files.get('pdfFile')
        if not file or not file.filename.lower().endswith('.pdf'): # type: ignore
            return "File tidak valid", 400
        input_path = os.path.join(UPLOAD_FOLDER, unique_filename('pdf'))
        output_path = os.path.join(UPLOAD_FOLDER, unique_filename('pdf'))
        file.save(input_path)
        try:
            doc = fitz.open(input_path)
            new_doc = fitz.open()
            for i in range(doc.page_count):
                page = doc.load_page(i)
                pix = page.get_pixmap(dpi=72) # type: ignore
                img_path = os.path.join(UPLOAD_FOLDER, unique_filename('jpg'))
                pix.save(img_path)
                img_pdf = fitz.open()
                rect = fitz.Rect(0, 0, pix.width, pix.height)
                page_pdf = img_pdf.new_page(width=pix.width, height=pix.height) # type: ignore
                page_pdf.insert_image(rect, filename=img_path)
                new_doc.insert_pdf(img_pdf)
                img_pdf.close()
                os.remove(img_path)
            new_doc.save(output_path)
            new_doc.close()
            doc.close()
            os.remove(input_path)
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return f"Gagal kompres PDF: {e}", 500
    return render_template('compress.html')

@app.route('/compress-premium', methods=['GET', 'POST'])
def compress_premium():
    if not session.get('user_id'):
        return redirect(url_for('signup', next='payment'))
    if not session.get('is_premium'):
        return redirect(url_for('payment'))
    if request.method == 'POST':
        file = request.files.get('pdfFile')
        if not file or not file.filename.lower().endswith('.pdf'): # type: ignore
            return "File tidak valid", 400
        input_path = os.path.join(UPLOAD_FOLDER, unique_filename('pdf'))
        output_path = os.path.join(UPLOAD_FOLDER, unique_filename('pdf'))
        file.save(input_path)
        try:
            doc = fitz.open(input_path)
            new_doc = fitz.open()
            for i in range(doc.page_count):
                page = doc.load_page(i)
                pix = page.get_pixmap(dpi=180) # type: ignore
                img_path = os.path.join(UPLOAD_FOLDER, unique_filename('jpg'))
                pix.pil_save(img_path, format="JPEG", optimize=True, quality=95)
                img_pdf = fitz.open()
                rect = fitz.Rect(0, 0, pix.width, pix.height)
                page_pdf = img_pdf.new_page(width=pix.width, height=pix.height) # type: ignore
                page_pdf.insert_image(rect, filename=img_path)
                new_doc.insert_pdf(img_pdf)
                img_pdf.close()
                os.remove(img_path)
            new_doc.save(output_path)
            new_doc.close()
            doc.close()
            os.remove(input_path)
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return f"Gagal kompres PDF premium: {e}", 500
    return render_template('compress_premium.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    next_page = request.args.get('next')
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        session['user_id'] = username
        flash('Sign up berhasil, silakan lanjut pembayaran.')
        if request.form.get('next'):
            return redirect(url_for(request.form.get('next'))) # type: ignore
        elif next_page:
            return redirect(url_for(next_page))
        return redirect(url_for('index'))
    return render_template('signup.html', next=next_page)

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/activate-premium', methods=['POST'])
def activate_premium():
    session['is_premium'] = True
    flash('Akun Anda sudah premium! Silakan gunakan fitur premium.')
    return redirect(url_for('compress_premium'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout.')
    return redirect(url_for('index'))

@app.route('/image-to-pdf', methods=['GET', 'POST'])
def image_to_pdf():
    if request.method == 'POST':
        files = request.files.getlist('imageFile')
        if not files or len(files) == 0:
            return "File gambar tidak ditemukan", 400
        try:
            doc = fitz.open()
            for file in files:
                image_path = os.path.join(UPLOAD_FOLDER, unique_filename('jpg'))
                file.save(image_path)
                img = Image.open(image_path).convert("RGB")
                img.save(image_path, "JPEG")
                pix = fitz.Pixmap(image_path)
                rect = fitz.Rect(0, 0, pix.width, pix.height)
                page = doc.new_page(width=pix.width, height=pix.height) # type: ignore
                page.insert_image(rect, filename=image_path)
                pix = None
                os.remove(image_path)
            output_pdf = os.path.join(UPLOAD_FOLDER, unique_filename('pdf'))
            doc.save(output_pdf)
            doc.close()
            return send_file(output_pdf, as_attachment=True)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Gagal konversi gambar ke PDF: {e}", 500
    return render_template('image_to_pdf.html')

@app.route('/remove-image', methods=['GET'])
def remove_image_page():
    return render_template('remove-image.html')

@app.route('/remove-background', methods=['POST'])
def remove_background():
    file = request.files.get('image')
    if not file or not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')): # type: ignore
        return "Gambar tidak ditemukan atau format tidak didukung", 400
    try:
        input_path = os.path.join(UPLOAD_FOLDER, unique_filename('png'))
        file.save(input_path)
        output_path = os.path.join(UPLOAD_FOLDER, unique_filename('png'))
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_image.save(output_path) # type: ignore
        result = send_file(output_path, as_attachment=True)
        os.remove(input_path)
        os.remove(output_path)
        return result
    except Exception as e:
        print("ERROR REMOVE BG:", e)
        return f"Gagal hapus background: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)