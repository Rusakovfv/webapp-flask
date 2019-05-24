from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'




class ReusableForm(Form):
    name = StringField('Name:', validators=[validators.required()])
    surname = StringField('Surname:', validators=[validators.required()])
    email = StringField('Email:', validators=[validators.required()])
    password = StringField('Password:', validators=[validators.required()])

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)

        print(form.errors)
        if request.method == 'POST':
            name = request.form['name']
            surname = request.form['surname']
            email = request.form['email']
            password = request.form['password']
            print(name, " ", email, " ")

        if form.validate():
            # Save the comment here.
            flash('Thanks for registration ' + name)
            file = open('files/storage.txt', "a", encoding='UTF-8')
            file.write(request.form['name']+';'+request.form['surname']+';'+request.form['email']+';'+request.form['password']+'\n')
            file.close()
        else:
            flash('Error: All the form fields are required. ')

        return render_template('index.html', form=form)

    @app.route("/viewdata")
    def viewdata():
        entities = list()
        with open("files/storage.txt", encoding="UTF-8") as f:
            for raw_line in f:
                data = raw_line.strip().split(';')
                entities.append({'name': data[0], 'surname': data[1], 'email': data[2], 'password': data[3]})
        return render_template('viewdata.html', entities=entities)

if __name__ == "__main__":
    app.run()