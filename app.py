from flask import Flask, render_template, request
from list_GLAMS import list_glams
from list_URL import list_url
from NationaalArchief import number_of_files

app = Flask(__name__)


@app.route('/result', methods=['POST'])
def receiveData():
    gname = request.form['glam_name']
    id = request.form['file_id']
    glam_list = list_glams
    try:
        for glam in glam_list:
            if glam['name'] == gname:
                break
    except:
        return "GLAM Not Found in the list"
    
    try:
        for url in list_url:
            gurl = url[gname]
    except:
        return "GLAM URL Not Found in the list"
    

    howManyMatches = number_of_files(id,gurl)
    print('In Progress')
    if howManyMatches == 0:
        return 'Sorry, no picture for given string exists!'
    else:
        returnString = 'Upload Successful'
        return returnString


@app.route('/', methods=['GET'])
def showForm():
    """Glam Form"""
    return render_template('glam_form.html')


if __name__ == "__main__":
    app.run()
