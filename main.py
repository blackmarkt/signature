from flask import Flask, request, render_template, url_for, redirect
import requests
from wtforms import Form, TextField, BooleanField, validators, PasswordField, HiddenField
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from PIL import Image, ImageDraw, ImageFont
import time
from binascii import a2b_base64
import os

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'MykEyisSUPERsecReT'


#Independent Functions and classes are all called first at the top
class SixthSub(Form):
    stu_name = TextField("Student name", [validators.Length(min=4, max=30)])
    hidden_f = HiddenField('')
    hidden_g = HiddenField('')


#Page routes and page function are called here second
@app.route("/")
def index():
    return render_template("index.html")

@csrf.exempt
@app.route("/sixth_form/", methods = ["GET", "POST"])
def sixth_form():
    try:
        form = SixthSub(request.form)

        if request.method == 'POST':
            #Gets student name from the post
            stu_name = form.stu_name.data
            #Gets the URI encoded image from the hidden field
            signat = form.hidden_f.data
            #Removes the first 22 un-needed chars from the string
            signat = signat[22:]
            #converts to binary
            binary_data = a2b_base64(signat)
            #Creates Image and save it in dir
            fd = open('/Users/jouwstrab/Desktop/Flask-Stu-Sign/static/image.png', 'wb')
            fd.write(binary_data)
            fd.close()
            #Gets the URI encoded image from the hidden field
            signature = form.hidden_g.data
            #Removes the first 22 un-needed chars from the string
            signature = signature[22:]
            #converts to binary
            binary_data = a2b_base64(signature)
            #Creates Image and save it in dir
            fd = open('/Users/jouwstrab/Desktop/Flask-Stu-Sign/static/image1.png', 'wb')
            fd.write(binary_data)
            fd.close()
            #Opens a blank copy of the form
            blank_form = Image.open('/Users/jouwstrab/Desktop/Flask-Stu-Sign/static/blank_form.jpg')
            #Loads the font
            arialFont = ImageFont.truetype('/Library/Fonts/Arial.ttf', 18)
            #Allows drawing
            draw = ImageDraw.Draw(blank_form)
            #Draw rectangle
            draw = ImageDraw.Draw(blank_form)
            draw.rectangle((416,1303,520,1363), fill='white')
            #Writes stu name
            draw.text((203,1328), stu_name, fill = 'black', font=arialFont)
            #Gets Current Time
            time_now = time.strftime("%m-%d-%Y")
            #Fills out data on form
            draw.text((912,1414), 'Date: ' + time_now, fill = 'black', font=arialFont)
            filename = stu_name + time_now + '.png'
            #Opens signature
            signature = Image.open('/Users/jouwstrab/Desktop/Flask-Stu-Sign/static/image.png')
            signatureone = Image.open('/Users/jouwstrab/Desktop/Flask-Stu-Sign/static/image1.png')
            blank_form.paste(signature, (702, 1298))
            blank_form.paste(signatureone, (327, 1402))
            blank_form.save('/Users/jouwstrab/Desktop/' + filename)
            os.remove('/Users/jouwstrab/Desktop/Flask-Stu-Sign/static/image.png')
            os.remove('/Users/jouwstrab/Desktop/Flask-Stu-Sign/static/image1.png')
            return redirect (url_for('index'))
        return render_template("sixth_form.html", form = form)

    except Exception as e:
        return(str(e))




if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
