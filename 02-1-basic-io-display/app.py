from flask import Flask, render_template, request, flash
from wtforms import Form, IntegerField, validators

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class input_form(Form):
    n = IntegerField('n: ', validators=[validators.NumberRange(min=1, max=20, message='Out of range(1-20)')])
    m = IntegerField('m: ', validators=[validators.NumberRange(min=1, max=20, message='Out of range(1-20)')])

    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = input_form(request.form)
        if request.method == 'POST' and form.validate():
            result = calculate(form.n.data, form.m.data)
        else:
            flash(form.errors)
            result = None
        return render_template('index.html', form=form, result=result)

def turn_to_string(x):
    while len(str(x)) < 4:
        x = ' '+str(x)
    return x

def calculate(n,m):
    result_matrix = [[0 for j in range(n)] for i in range(m)]

    max_number = n*m
    start_number = 1
    x = 0
    y = 0
    step_number = 0
    while start_number <= max_number:
        # right
        if start_number <= max_number:
            for i in range(x + step_number, n):
                result_matrix[x + step_number][i] = turn_to_string(start_number)
                start_number += 1
        y += 1
        # down
        if start_number <= max_number:
            for i in range(y + step_number, m):
                result_matrix[i][n - 1] = turn_to_string(start_number)
                start_number += 1
        x -= 1
        # left
        if start_number <= max_number:
            for i in range(n - 2, x + step_number, -1):
                result_matrix[m-1][i] = turn_to_string(start_number)
                start_number += 1
        y -= 1
        # up
        if start_number <= max_number:
            for i in range(m - 2, y + step_number, -1):
                result_matrix[i][y + step_number] = turn_to_string(start_number)
                start_number += 1
        x += 1
        step_number += 1
        n -= 1
        m -= 1
    result = list()
    for raw in result_matrix:
        raw_text = ''
        for column in raw:
            raw_text = raw_text + column
        result.append(raw_text)
    return result



if __name__ == '__main__':
    app.run(debug=True)
