__author__ = "Joseph Mullen"

from personal_web.personalWebsite import app
from flask import render_template, request, flash
from personal_web.forms import queryForm
from personal_web.core.virtuoso import Repository
from examplequeries import examples

'''Page routes'''

@app.route('/')
def index():
    return render_template('index.html', title="Home")

@app.route('/datasets' , methods=['GET', 'POST'])
def datasets():
    if request.method == 'POST':
        e = examples()
        rep = Repository('dba', 'dba', 'http://drenin', 'http://drenin', 'http://drenin.ncl.ac.uk:8890/sparql', False)
        result = "NONE"
        try:
            result = rep.sparql_query(request.form.get('sparql'))
        except Exception as E:
            flash('{} {}'.format('Problem with SPARQL Query!\n', str(E)))
            return render_template('datasets.html', title="Query", form=queryForm(), reslen=0, examples=e.getquery())
        tableheads = ""
        # sort out below- not ok
        if len(result) > 0:
            for f in result:
                tableheads = f
        return render_template('datasets.html', title="Query", form=queryForm(), results=result, tableheads=tableheads, reslen=len(result), examples = e.getquery())
    e = examples()
    return render_template('datasets.html', title="Query", form=queryForm(), reslen=0, examples = e.getquery())




