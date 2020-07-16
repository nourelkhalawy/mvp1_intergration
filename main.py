import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from os import environ
import requests
import glob
import sys
import shutil


# Google Cloud Storage
bucketName = 'mvp_images'
bucketFolder = 'uploads/'

#set credentials
credential_path = "credentials.json"
environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


app = Flask(__name__)

# app.config['UPLOAD_FOLDER'] = bucketFolder
app.config['ALLOWED_EXTENSIONS'] = set([ 'png', 'jpg', 'jpeg', 'JPG'])

# storage_client = storage.Client()
# bucket = storage_client.get_bucket(bucketName)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


#files = glob.glob('cyclegan\\datasets\\dataset\\testA')
#for f in files:
    #os.remove(f)
app.config['UPLOAD_FOLDER'] = "static\\uploads"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        #src=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #file.save(src)
        dataset_pathA="static\\cyclegan\\datasets\\dataset\\testA"
        dataset_pathB="static\\cyclegan\\datasets\\dataset\\testB"
        if os.path.isdir(dataset_pathA):
            shutil.rmtree(dataset_pathA)
            os.mkdir(dataset_pathA)
            print("emptied testA")
        if os.path.isdir(dataset_pathB):
            shutil.rmtree(dataset_pathB)
            os.mkdir(dataset_pathB)
            print("emptied testB")
        test_folder_pathA=os.path.join(dataset_pathA, filename)
        test_folder_pathB=os.path.join(dataset_pathB, filename)
        file.save(test_folder_pathA)
        #file.save(test_folder_pathB)

        result_path="static\\results\\selfie2anime\\test_latest\\images"
        if os.path.isdir(result_path):
            shutil.rmtree(result_path)
            #os.mkdir("static\\results\\selfie2anime\\test_latest\\images")

        

    sys.path.insert(1, 'static\cyclegan')
    import test

    return render_template("painter.html", image_source=os.path.join(result_path,os.listdir(result_path)[0]))



if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("5000"),
        debug=True
    )
