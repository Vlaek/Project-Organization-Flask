from flask import Flask, render_template, request, redirect
from config import hostname, user, password, db_name, port
import pymysql
from datetime import date, datetime

app = Flask(__name__)
app.debug = True

db = pymysql.connect(host=hostname,
                     port=port,
                     user=user,
                     password=password,
                     database=db_name,
                     cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def index():
    return render_template('index.html')


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


@app.route('/Workers', methods=['POST', 'GET'])
def workers():
    if request.method == "POST":
        vorname = request.form['Vorname']
        nachname = request.form['Nachname']
        dob = request.form['DOB']
        speciality = request.form['speciality']
        position = request.form['position']

        cursor = db.cursor()

        insert_query = "INSERT INTO `Workers` (idWorker, Nachname, Vorname, DOB, Speciality, Position) " \
                       "VALUES ('" + str(21) + "', '" + nachname + "', '" + vorname + "', '" + dob + "', '" + speciality + "', '" + position + "');"
        cursor.execute(insert_query)
        db.commit()

        return redirect('/Workers')

    else:
        cursor = db.cursor()
        sql = 'SELECT * FROM Workers'
        cursor.execute(sql)
        results = cursor.fetchall()

        length = len(results)

        old_date = []

        for i in range(length):
            results[i].update({'Age': calculate_age(results[i]['DOB'])})
            old_date.append(results[i]['DOB'].strftime('%d.%m.%Y'))

        for i in range(length):
            results[i].pop('DOB')
            results[i].update({'DOB': old_date[i]})

        return render_template('Workers.html', results=results, length=length)


@app.route('/Projects')
def projects():
    cursor = db.cursor()

    cursor.execute(
        'SELECT Workers.Nachname, Workers.Vorname, Projects.idProject, Projects.Name, Projects.StartDate, Projects.EndDate, '
        'Projects.Equipment, Projects.Cost FROM Workers INNER JOIN Projects ON Workers.idWorker = '
        'Projects.Leader')
    results = cursor.fetchall()

    project_sum = 0
    length = len(results)

    for i in range(length):
        project_sum += int(results[i]['Cost'])

    return render_template('Projects.html', results=results, length=length, project_sum=project_sum)


@app.route('/Contracts')
def contracts():
    cursor = db.cursor()

    cursor.execute('SELECT Contracts.idContract, Min(Projects.StartDate) AS MinStartDate, Max(Projects.EndDate) AS '
                   'MaxEndDate, Contracts.Name, Contracts.Client, Sum(Projects.Cost) AS FullCost FROM Projects INNER '
                   'JOIN (Contracts INNER JOIN ContractProject ON Contracts.IdContract = ContractProject.IdContract) '
                   'ON Projects.IdProject = ContractProject.IdProject GROUP BY Contracts.IdContract, Contracts.Name, '
                   'Contracts.Client')

    results = cursor.fetchall()

    total_sum = 0
    length = len(results)

    for i in range(length):
        total_sum += int(results[i]['FullCost'])

    return render_template('Contracts.html', results=results, length=length, total_sum=total_sum)


@app.route('/Equipments')
def equipments():
    cursor = db.cursor()
    sql = 'SELECT * FROM Workers'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('Equipments.html', results=results)


@app.route('/EquipmentsProjects')
def equipments_projects():
    cursor = db.cursor()
    sql = 'SELECT * FROM Workers'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('EquipmentsProjects.html', results=results)


@app.route('/Subcontractors')
def subcontractors():
    cursor = db.cursor()
    sql = 'SELECT * FROM Workers'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('Subcontractors.html', results=results)


if __name__ == '__main__':
    app.run()
