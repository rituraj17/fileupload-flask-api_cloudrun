from flask import Flask,request
from component import  storage_component
import os 
import json
app = Flask(__name__)

# Below 2 lines are used to define a path where files will be uploaded only for local 
UPLOAD_FOLDER = os.getcwd()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Reading config parameters
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(PROJECT_ROOT, 'config.json')
with open(CONFIG_PATH, 'r') as config_obj:
    config = json.loads(config_obj.read())
bucket_name=config["Storage"]["bucket_name"]

storage_comp = storage_component.StorageComponent()

@app.route("/")
def hello_function():
    """ This function is to test the API if its working or not 

    Returns:
        String: The return string can be anything.Needed it to test the intial API
    """    
    try:
        return " hello world"
    except Exception as e:
        return e

@app.route("/uploader",methods = ['POST'])
def file_upload():
    """ This function  task is to upload the files to the gcs bucket by downloading the 
        data to server 

    Returns:
        [String]: [200 Response] -- file has been uploaded properly 
                  [200 Response] -- if get request parameter is provided 
    """    
    try:
        if request.method == 'POST':
            f=request.files['file']
            fname=f.filename
            # print(fname)
            # print(UPLOAD_FOLDER)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            filepath=UPLOAD_FOLDER + "/" +fname
            # print(filepath)
            destination_path=fname
            storage_comp.upload_blob(bucket_name,filepath,destination_path)
            if os.path.exists(filepath):
                os.remove(filepath)
            else:
                print("The file does not exist")
            return " file uploaded successfully"
        else:
            return " Does not support GET request"
    except Exception as e:
        return e


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))