from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
import os
import re
 
 
app = Flask(__name__)
 
 
DOWNLOAD_DIRECTORY = "downloads"
 
 
if not os.path.exists(DOWNLOAD_DIRECTORY):
   os.makedirs(DOWNLOAD_DIRECTORY)
 
 
def sanitize_filename(filename):
   # Replace invalid characters with underscores
   return re.sub(r'[<>:"/\\|?*]', '_', filename)
 
 
@app.route('/')
def index():
   return render_template('index.html')
 
 
@app.route('/download', methods=['POST'])
def download():
   url = request.form['url']
   print("Received URL:", url)
   try:
       yt = YouTube(url)
       print("Video Title:", yt.title)
       stream = yt.streams.get_highest_resolution()
       title = sanitize_filename(yt.title)
       filename = f"{title}.mp4"
       filepath = os.path.join(DOWNLOAD_DIRECTORY, filename)
       print("Downloading...")
       stream.download(output_path=DOWNLOAD_DIRECTORY, filename=filename)
       print("Download Complete.")
       return send_file(filepath, as_attachment=True)
   except Exception as e:
       print("Error:", str(e))
       return render_template('error.html', error=str(e))
 
 
if __name__ == '__main__':
   app.run(debug=True)
