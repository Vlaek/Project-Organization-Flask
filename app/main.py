from flask import Flask, render_template, request, redirect
import pymysql
from config import hostname, user, password, db_name, port
from datetime import date

app = Flask(__name__)
app.debug = True

db = pymysql.connect(
    host=hostname,
    port=port,
    user=user,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Workers', methods=['POST', 'GET'])
def workers():
    if request.method == "POST":
        if request.form['action'] == 'Добавить':
            forename = request.form['forename']
            surname = request.form['surname']
            dob = request.form['DOB']
            speciality = request.form['speciality']
            position = request.form['position']
            executor = request.form.getlist('projects')

            cursor = db.cursor()

            insert_query = "INSERT INTO `Workers` (surname, forename, DOB, Speciality, Position) " \
                           "VALUES ('" + surname + "', '" + forename + "', '" + dob + "', '" + speciality + "', '" + position + "');"

            cursor.execute(insert_query)

            db.commit()

            cursor.execute("SELECT * FROM Workers")

            results = cursor.fetchall()

            ids_workers = []

            for i in range(len(results)):
                ids_workers.append(results[i]['idWorker'])

            for row in range(len(executor)):
                insert_query = "INSERT INTO `Executors` (idProject, idWorker) " \
                               "VALUES ('" + str(executor[row]) + "', '" + str(max(ids_workers)) + "');"
                print('Добавлен')
                cursor.execute(insert_query)
                db.commit()

            return redirect('/Workers')

        elif request.form['action'] == 'Изменить':

            id2 = request.form['id2']
            forename2 = request.form['forename2']
            surname2 = request.form['surname2']
            dob2 = request.form['DOB2']
            speciality2 = request.form['speciality2']
            position2 = request.form['position2']
            executor2 = request.form.getlist('projects2')

            print(executor2);

            cursor = db.cursor()

            update_query = "UPDATE Workers SET " \
                           "Surname ='" + surname2 + "', Forename='" + forename2 + \
                           "', DOB='" + dob2 + "', Speciality='" + speciality2 + \
                           "', Position='" + position2 + "' WHERE idWorker='" + str(id2) + "';"

            cursor.execute(update_query)

            db.commit()

            cursor.execute('DELETE FROM Executors WHERE ((Executors.idWorker=' + str(id2) + '))')

            db.commit()

            ids_workers = []

            cursor.execute("SELECT * FROM Workers")

            results = cursor.fetchall()

            for i in range(len(results)):
                ids_workers.append(results[i]['idWorker'])

            for row in range(len(executor2)):
                print('da', str(executor2[row]))
                insert_query = "INSERT INTO `Executors` (idProject, idWorker) " \
                               "VALUES ('" + str(executor2[row]) + "', '" + str(id2) + "');"
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

        new_date = []

        for i in range(len(results)):
            results[i].update({'Age': calculate_age(results[i]['DOB'])})
            new_date.append(results[i]['DOB'].strftime('%d.%m.%Y'))

        for i in range(len(results)):
            results[i].pop('DOB')
            results[i].update({'DOB': new_date[i]})

        sql_engineer = "SELECT Count(Workers.Speciality) AS ENGINEERS FROM Workers WHERE Workers.Speciality = 'Инженер'"
        sql_technician = "SELECT Count(Workers.Speciality) AS TECHNICIAN FROM Workers WHERE Workers.Speciality = 'Техник'"
        sql_assistant = "SELECT Count(Workers.Speciality) AS ASSISTANT FROM Workers WHERE Workers.Speciality = 'Лаборант'"
        sql_constructor = "SELECT Count(Workers.Speciality) AS CONSTRUCTOR FROM Workers WHERE Workers.Speciality = 'Конструктор'"
        sql_staff = "SELECT Count(Workers.Speciality) AS STAFF FROM Workers WHERE Workers.Speciality = 'Обслуживающий персонал'"
        sql_worker = "SELECT Count(Workers.Position) AS WORKER FROM Workers WHERE Workers.Position = 'Рабочий'"
        sql_leader = "SELECT Count(Workers.Position) AS LEADER FROM Workers WHERE Workers.Position = 'Начальник'"

        cursor.execute(sql_engineer)
        count_engineers = cursor.fetchall()

        cursor.execute(sql_technician)
        count_technicians = cursor.fetchall()

        cursor.execute(sql_assistant)
        count_assistants = cursor.fetchall()

        cursor.execute(sql_constructor)
        count_constructors = cursor.fetchall()

        cursor.execute(sql_staff)
        count_staffs = cursor.fetchall()

        cursor.execute(sql_worker)
        count_workers = cursor.fetchall()

        cursor.execute(sql_leader)
        count_leaders = cursor.fetchall()

        cursor.execute(
            "SELECT Projects.idProject, Projects.Name, Workers.idWorker FROM Workers INNER JOIN (Projects INNER "
            "JOIN Executors ON Projects.idProject = Executors.idProject) "
            "ON Workers.idWorker = Executors.idWorker ")

        executors_check = cursor.fetchall()

        cursor.execute("SELECT * FROM Projects")

        projects_check = cursor.fetchall()

        edit_executors_check = []

        for i in range(len(projects_check)):
            edit_executors_check.append(projects_check[i]['name'])

        return render_template('Workers.html', results=results, length=len(results),
                               count_engineers=count_engineers,
                               count_technicians=count_technicians, count_assistants=count_assistants,
                               count_constructors=count_constructors, count_staffs=count_staffs,
                               count_workers=count_workers, count_leaders=count_leaders,
                               executors_check=executors_check,
                               projects_check=projects_check)


@app.route('/Worker/delete/<int:worker_id>')
def worker_delete(worker_id):
    cursor = db.cursor()

    cursor.execute('DELETE FROM Workers WHERE ((Workers.idWorker=' + str(worker_id) + '))')

    db.commit()

    return redirect('/Workers')

@app.route('/Projects', methods=['POST', 'GET'])
def projects():
    if request.method == "POST":
        if request.form['action'] == 'Добавить':

            name = request.form['Name']
            cost = request.form['Cost']
            start_date = request.form['StartDate']
            end_date = request.form['EndDate']
            leader = request.form['Leader']

            cursor = db.cursor()

            name_leader = leader.split(" ")

            sql = "SELECT Workers.Surname, Workers.Forename, Workers.idWorker " \
                  "FROM WORKERS " \
                  "GROUP BY Workers.Surname, Workers.Forename, Workers.idWorker " \
                  "HAVING (((Workers.Surname)='" + name_leader[1] + "') AND ((Workers.Forename)='" + name_leader[0] + "'))"

            cursor.execute(sql)

            id_leader = cursor.fetchall()

            insert_query = "INSERT INTO `Projects` (name, startDate, endDate, cost, leader) " \
                           "VALUES ('" + name + "', '" + start_date + "', '" + end_date + "', '" + cost + "', '" + str(id_leader[0]["idWorker"]) + "');"

            cursor.execute(insert_query)

            db.commit()

            return redirect('/Projects')

        elif request.form['action'] == 'Изменить':

            id2 = request.form['idProject2']
            name2 = request.form['Name2']
            cost2 = request.form['Cost2']
            equipment2 = request.form['Equipment2']
            start_date2 = request.form['StartDate2']
            end_date2 = request.form['EndDate2']
            leader2 = request.form['Leader2']

            cursor = db.cursor()

            name_leader = leader2.split(" ")

            sql = "SELECT Workers.Surname, Workers.Forename, Workers.idWorker " \
                  "FROM WORKERS " \
                  "GROUP BY Workers.Surname, Workers.Forename, Workers.idWorker " \
                  "HAVING (((Workers.Surname)='" + name_leader[1] + "') AND ((Workers.Forename)='" + name_leader[0] + "'))"

            cursor.execute(sql)

            id_leader2 = cursor.fetchall()

            insert_query = "UPDATE Projects SET " \
                           "Name ='" + name2 + "', Cost='" + cost2 + \
                           "', Equipment='" + equipment2 + "', StartDate='" + start_date2 + \
                           "', EndDate='" + end_date2 + "', Leader='" + str(id_leader2[0]["idWorker"]) + "' WHERE idProject='" + str(id2) + "'"

            cursor.execute(insert_query)

            db.commit()

            return redirect('/Projects')
    else:

        cursor = db.cursor()

        q = request.args.get('q')

        if q:
            sql = "SELECT Workers.Surname, Workers.Forename, Projects.idProject, Projects.Name, Projects.StartDate, " \
                  "Projects.EndDate, Projects.Cost FROM Workers INNER JOIN Projects ON Workers.idWorker = " \
                  "Projects.Leader WHERE ((Workers.Surname LIKE '%" + q + "%') OR (Workers.Forename LIKE '%" + q + "%')" \
                  " OR (Projects.Name LIKE '%" + q + "%') OR (Projects.Equipment LIKE '%" + q + "%')" \
                  " OR (Projects.StartDate LIKE '%" + q + "%') OR (Projects.EndDate LIKE '%" + q + "%') OR (Projects.Cost LIKE '%" + q + "%'))"
        else:
            sql = "SELECT Workers.Surname, Workers.Forename, Projects.idProject, Projects.Name, Projects.StartDate, " \
                  "Projects.EndDate, Projects.Cost FROM Workers INNER JOIN Projects ON Workers.idWorker = " \
                  "Projects.Leader"

        cursor.execute(sql)

        results = cursor.fetchall()

        project_sum = 0

        for i in range(len(results)):
            project_sum += results[i]['Cost']

        cursor.execute("SELECT Workers.Surname, Workers.Forename FROM Workers WHERE Workers.Position = 'Начальник'")

        leaders = cursor.fetchall()

        new_start_date = []
        new_end_date = []

        for i in range(len(results)):
            new_start_date.append(results[i]['StartDate'].strftime('%d.%m.%Y'))
            new_end_date.append(results[i]['EndDate'].strftime('%d.%m.%Y'))

        for i in range(len(results)):
            results[i].pop('StartDate')
            results[i].update({'StartDate': new_start_date[i]})
            results[i].pop('EndDate')
            results[i].update({'EndDate': new_end_date[i]})

        return render_template('Projects.html', results=results, length=len(results), project_sum=project_sum, leaders=leaders)


@app.route('/Project/delete/<int:project_id>')
def project_delete(project_id):
    cursor = db.cursor()

    cursor.execute('DELETE FROM Projects WHERE ((Projects.idProject=' + str(project_id) + '))')

    db.commit()

    return redirect('/Projects')


@app.route('/Contracts', methods=['POST', 'GET'])
def contracts():
    if request.method == "POST":
        if request.form['action'] == 'Добавить':

            name = request.form['Name']
            client = request.form['Client']
            contract_project = request.form.getlist('projects')

            cursor = db.cursor()

            insert_query = "INSERT INTO `Contracts` (Name, Client) " \
                           "VALUES ('" + name + "', '" + client + "');"

            cursor.execute(insert_query)

            db.commit()

            cursor.execute("SELECT * FROM Contracts")

            results = cursor.fetchall()

            ids_contracts = []

            for i in range(len(results)):
                ids_contracts.append(results[i]['idContract'])

            for row in range(len(contract_project)):
                insert_query = "INSERT INTO `ContractProject` (idContract, idProject) " \
                               "VALUES ('" + str(max(ids_contracts)) + "', '" + str(contract_project[row]) + "');"
                cursor.execute(insert_query)
                db.commit()

            return redirect('/Contracts')

        elif request.form['action'] == 'Изменить':

            id2 = request.form['idContract2']
            name2 = request.form['Name2']
            client2 = request.form['Client2']
            contract_project2 = request.form.getlist('projects2')

            cursor = db.cursor()

            update_query = "UPDATE Contracts SET " \
                           "Name ='" + name2 + "', Client='" + client2 + \
                           "' WHERE idContract='" + str(id2) + "'"

            cursor.execute(update_query)

            cursor.execute('DELETE FROM ContractProject WHERE ((ContractProject.idContract=' + str(id2) + '))')

            db.commit()

            ids_contracts = []

            cursor.execute("SELECT * FROM Contracts")

            results = cursor.fetchall()

            for i in range(len(results)):
                ids_contracts.append(results[i]['idContract'])

            for row in range(len(contract_project2)):
                insert_query = "INSERT INTO `ContractProject` (idContract, idProject) " \
                               "VALUES ('" + str(id2) + "', '" + str(contract_project2[row]) + "');"
                cursor.execute(insert_query)
                db.commit()

            return redirect('/Contracts')
    else:

        cursor = db.cursor()

        q = request.args.get('q')

        if q:
            sql = "SELECT Contracts.idContract, Min(Projects.StartDate) AS MinStartDate, Max(Projects.EndDate) AS " \
                  "MaxEndDate, Contracts.Name, Contracts.Client, Sum(Projects.Cost) AS FullCost FROM Projects INNER " \
                  "JOIN (Contracts INNER JOIN ContractProject ON Contracts.IdContract = ContractProject.IdContract) " \
                  "ON Projects.IdProject = ContractProject.IdProject " \
                  "WHERE ((Contracts.Name LIKE '%" + q + "%') OR (Contracts.Client LIKE '%" + q + "%')) " \
                  "GROUP BY Contracts.IdContract, Contracts.Name, Contracts.Client"
        else:
            sql = "SELECT Contracts.idContract, Min(Projects.StartDate) AS MinStartDate, Max(Projects.EndDate) AS " \
                  "MaxEndDate, Contracts.Name, Contracts.Client, Sum(Projects.Cost) AS FullCost FROM Projects INNER " \
                  "JOIN (Contracts INNER JOIN ContractProject ON Contracts.IdContract = ContractProject.IdContract) " \
                  "ON Projects.IdProject = ContractProject.IdProject GROUP BY Contracts.IdContract, Contracts.Name, " \
                  "Contracts.Client"

        cursor.execute(sql)

        results = cursor.fetchall()

        total_sum = 0

        for i in range(len(results)):
            total_sum += results[i]['FullCost']

        new_start_date = []
        new_end_date = []

        for i in range(len(results)):
            new_start_date.append(results[i]['MinStartDate'].strftime('%d.%m.%Y'))
            new_end_date.append(results[i]['MaxEndDate'].strftime('%d.%m.%Y'))

        for i in range(len(results)):
            results[i].pop('MinStartDate')
            results[i].update({'MinStartDate': new_start_date[i]})
            results[i].pop('MaxEndDate')
            results[i].update({'MaxEndDate': new_end_date[i]})

        cursor.execute("SELECT * FROM Projects")

        projects_check = cursor.fetchall()

        cursor.execute("SELECT Projects.idProject, Projects.Name, Contracts.idContract FROM Contracts INNER JOIN (Projects INNER "
                       "JOIN ContractProject ON Projects.idProject = ContractProject.idProject) "
                       "ON Contracts.idContract = ContractProject.idContract ")

        contract_project_check = cursor.fetchall()

        edit_projects_check = []

        for i in range(len(projects_check)):
            edit_projects_check.append(projects_check[i]['Name'])

        return render_template('Contracts.html', results=results, length=len(results), total_sum=total_sum,
                               projects_check=projects_check, contract_project_check=contract_project_check,
                               edit_projects_check=edit_projects_check)


@app.route('/Contract/delete/<int:contract_id>')
def contract_delete(contract_id):

    cursor = db.cursor()

    cursor.execute('DELETE FROM Contracts WHERE ((Contracts.idContract=' + str(contract_id) + '))')

    cursor.execute('DELETE FROM ContractProject WHERE ((ContractProject.idContract=' + str(contract_id) + '))')

    db.commit()

    return redirect('/Contracts')


@app.route('/Subcontractors', methods=['POST', 'GET'])
def subcontractors():
    if request.method == "POST":
        if request.form['action'] == 'Добавить':

            name = request.form['Name']
            cost = request.form['Cost']
            name_project = request.form['NameProject']
            workload = request.form['Workload']

            cursor = db.cursor()

            id_project_query = "SELECT Projects.Name, Projects.idProject FROM Projects" \
                               " Where (((Projects.Name)='" + name_project + "'))"

            cursor.execute(id_project_query)

            id_project = cursor.fetchall()

            insert_query = "INSERT INTO `Subcontractors` (Name, Cost, idProject, Workload) " \
                           "VALUES ('" + name + "', '" + cost + "', '" + str(id_project[0]['idProject']) + "', '" + workload + "')"
            cursor.execute(insert_query)
            db.commit()

            return redirect('/Subcontractors')

        elif request.form['action'] == 'Изменить':

            id2 = request.form['idSubcontractor2']
            name2 = request.form['Name2']
            cost2 = request.form['Cost2']
            name_project2 = request.form['NameProject2']
            workload2 = request.form['Workload2']

            cursor = db.cursor()

            id_project_query = "SELECT Projects.Name, Projects.idProject FROM Projects INNER JOIN Subcontractors" \
                               " ON Projects.idProject = Subcontractors.idProject " \
                               " Where (((Projects.Name)='" + name_project2 + "'))"

            cursor.execute(id_project_query)

            id_project2 = cursor.fetchall()

            update_query = "UPDATE Subcontractors SET " \
                           " Name = '" + name2 + "', Cost = '" + cost2 + "', " \
                           " idProject='" + str(id_project2[0]['idProject']) + "', Workload='" + workload2 + "' " \
                           " WHERE (idSubcontractor='" + str(id2) + "')"
            cursor.execute(update_query)

            db.commit()

            return redirect('/Subcontractors')

    else:

        cursor = db.cursor()

        q = request.args.get('q')

        if q:
            sql = "SELECT Subcontractors.Name, Projects.Name AS ProjectName, Subcontractors.Cost, Subcontractors.Workload, Subcontractors.idSubcontractor " \
                  "FROM Projects INNER JOIN " \
                  "Subcontractors ON Projects.idProject = Subcontractors.idProject " \
                  "WHERE ((Subcontractors.Name LIKE '%" + q + "%') OR " \
                  "(Subcontractors.Cost LIKE '%" + q + "%') OR " \
                  "(Subcontractors.Workload LIKE '%" + q + "%') OR " \
                  "(Projects.Name LIKE '%" + q + "%'))"
        else:
            sql = "SELECT * FROM Subcontractors"

        cursor.execute(sql)

        results = cursor.fetchall()

        total_sum = 0

        for i in range(len(results)):
            total_sum += results[i]['Cost']

        sql_project = "SELECT Projects.idProject, Projects.Name " \
                      "FROM Projects"

        cursor.execute(sql_project)

        projects_name = cursor.fetchall()

        for i in range(len(results)):
            results[i].update({'ProjectName': projects_name[i]['Name']})

        return render_template('Subcontractors.html', results=results, length=len(results), total_sum=total_sum, projects_name=projects_name)


@app.route('/Subcontractor/delete/<int:subcontractor_id>')
def subcontractor_delete(subcontractor_id):

    cursor = db.cursor()

    cursor.execute('DELETE FROM Subcontractors WHERE ((Subcontractors.idSubcontractor=' + str(subcontractor_id) + '))')

    db.commit()

    return redirect('/Subcontractors')


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


if __name__ == '__main__':
    app.run(debug=True)
