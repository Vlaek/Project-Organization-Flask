from flask import Flask, render_template, request, redirect
from config import hostname, user, password, db_name, port
import pymysql
from datetime import date

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
        if request.form['action'] == 'Добавить':
            forename = request.form['forename']
            surname = request.form['surname']
            dob = request.form['DOB']
            speciality = request.form['speciality']
            position = request.form['position']

            cursor = db.cursor()

            insert_query = "INSERT INTO `Workers` (surname, forename, DOB, Speciality, Position) " \
                           "VALUES ('" + surname + "', '" + forename + "', '" + dob + "', '" + speciality + "', '" + position + "');"
            cursor.execute(insert_query)
            db.commit()

            return redirect('/Workers')
        elif request.form['action'] == 'Изменить':
            id2 = request.form['Worker2']
            forename2 = request.form['Forename2']
            surname2 = request.form['Surname2']
            dob2 = request.form['DOB2']
            speciality2 = request.form['Speciality2']
            position2 = request.form['Position2']

            cursor = db.cursor()

            insert_query = "UPDATE Workers SET " \
                           "Surname ='" + surname2 + "', Forename='" + forename2 + \
                           "', DOB='" + dob2 + "', Speciality='" + speciality2 + \
                           "', Position='" + position2 + "' WHERE idWorker='" + str(id2) + "';"
            cursor.execute(insert_query)
            db.commit()

            return redirect('/Workers')
    else:

        cursor = db.cursor()
        q = request.args.get('q')

        if q:
            sql = "SELECT * FROM Workers WHERE ((Surname LIKE '%" + q + "%')" \
                  "OR (Forename LIKE '%" + q + "%')" \
                  "OR (DOB LIKE '%" + q + "%')" \
                  "OR (Speciality LIKE '%" + q + "%')" \
                  "OR (Position LIKE '%" + q + "%'))"
        else:
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


@app.route('/Worker/delete/<int:worker_id>')
def worker_delete(worker_id):

    cursor = db.cursor()

    sql = 'DELETE FROM Workers WHERE ((Workers.idWorker=' + str(worker_id) + '))'

    cursor.execute(sql)

    return redirect('/Workers')


@app.route('/Projects')
def projects():
    cursor = db.cursor()

    cursor.execute(
        'SELECT Workers.Surname, Workers.Forename, Projects.idProject, Projects.Name, Projects.StartDate, '
        'Projects.EndDate, Projects.Equipment, Projects.Cost FROM Workers INNER JOIN Projects ON Workers.idWorker = '
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
