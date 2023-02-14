from flask import Flask, request, redirect, render_template, send_from_directory
import ffmpeg
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)

    input_file = file.filename
    output_file = os.path.splitext(input_file)[0] + ".gif"

    file.save(input_file)
    convert_format(input_file, output_file)

    return f"<a href='/download/{output_file}'>Download {output_file}</a>"


def convert_format(input_file, output_file):
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, output_file, format='gif')
    ffmpeg.run(stream)


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(".", filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
