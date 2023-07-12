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
            projects_list = request.form.getlist('projects')

            cursor = db.cursor()

            query = "INSERT INTO `Workers` (surname, forename, DOB, Speciality, Position) " \
               "VALUES ('" + surname + "', '" + forename + "', '" + dob + "', '" + speciality + "', '" + position + "')"

            cursor.execute(query)

            cursor.execute("SELECT * FROM Workers")

            last_id = cursor.fetchall()[-1]['idWorker']

            for project_id in projects_list:
                insert_query = "INSERT INTO `Executors` (idProject, idWorker) " \
                               "VALUES ('" + str(project_id) + "', '" + str(last_id) + "')"
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
            projects_list2 = request.form.getlist('projects2')

            cursor = db.cursor()

            query = "UPDATE Workers SET " \
               "surname ='" + surname2 + "', forename='" + forename2 + \
               "', DOB='" + dob2 + "', speciality='" + speciality2 + \
               "', position='" + position2 + "' WHERE idWorker='" + str(id2) + "';"

            cursor.execute(query)

            cursor.execute('DELETE FROM Executors WHERE (Executors.idWorker=' + str(id2) + ')')

            for project in projects_list2:
                query = "INSERT INTO `Executors` (idProject, idWorker) " \
                        "VALUES ('" + str(project) + "', '" + str(id2) + "');"
                cursor.execute(query)

            db.commit()

            return redirect('/Workers')
    else:
        cursor = db.cursor()
        q = request.args.get('q')

        if q:
            sql = "SELECT * FROM Workers WHERE ((surname LIKE '%" + q + "%')" \
                "OR (forename LIKE '%" + q + "%')" \
                "OR (DOB LIKE '%" + q + "%')" \
                "OR (speciality LIKE '%" + q + "%')" \
                "OR (position LIKE '%" + q + "%'))"
        else:
            sql = 'SELECT * FROM Workers'

        cursor.execute(sql)

        workers_list = cursor.fetchall()

        for worker in workers_list:
            worker.update({'Age': calculate_age(worker['DOB'])})
            worker.update({'DOB': worker['DOB'].strftime('%d.%m.%Y')})

        sql_engineer = "SELECT Count(Workers.Speciality) AS ENGINEERS FROM Workers WHERE Workers.speciality = 'Инженер'"
        sql_technician = "SELECT Count(Workers.Speciality) AS TECHNICIAN FROM Workers WHERE Workers.speciality = 'Техник'"
        sql_assistant = "SELECT Count(Workers.Speciality) AS ASSISTANT FROM Workers WHERE Workers.speciality = 'Лаборант'"
        sql_constructor = "SELECT Count(Workers.Speciality) AS CONSTRUCTOR FROM Workers WHERE Workers.speciality = 'Конструктор'"
        sql_staff = "SELECT Count(Workers.Speciality) AS STAFF FROM Workers WHERE Workers.speciality = 'Обслуживающий персонал'"
        sql_worker = "SELECT Count(Workers.Position) AS WORKER FROM Workers WHERE Workers.position = 'Рабочий'"
        sql_leader = "SELECT Count(Workers.Position) AS LEADER FROM Workers WHERE Workers.position = 'Начальник'"

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
            "ON Workers.idWorker = Executors.idWorker")

        executors_list = cursor.fetchall()

        cursor.execute("SELECT * FROM Projects")

        projects_list = cursor.fetchall()

        cursor.execute("SELECT Projects.leader FROM Projects")
        leader_list = []

        for i in cursor.fetchall():
            leader_list.append(i['leader'])

        return render_template('Workers.html', workers_list=workers_list, length=len(workers_list),
                               count_engineers=count_engineers,
                               count_technicians=count_technicians, count_assistants=count_assistants,
                               count_constructors=count_constructors, count_staffs=count_staffs,
                               count_workers=count_workers, count_leaders=count_leaders,
                               executors_list=executors_list,
                               projects_list=projects_list, leader_list=leader_list)


@app.route('/Worker/delete/<int:worker_id>')
def worker_delete(worker_id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM Executors WHERE (Executors.idWorker=' + str(worker_id) + ')')
    cursor.execute('DELETE FROM Workers WHERE (Workers.idWorker=' + str(worker_id) + ')')
    db.commit()
    return redirect('/Workers')


@app.route('/Projects', methods=['POST', 'GET'])
def projects():
    if request.method == "POST":
        if request.form['action'] == 'Добавить':
            name = request.form['name']
            cost = request.form['cost']
            start_date = request.form['startDate']
            end_date = request.form['endDate']
            leader = request.form['leader']

            cursor = db.cursor()

            id_leader = leader.split("leader-")

            sql = "SELECT Workers.surname, Workers.forename, Workers.idWorker " \
                  "FROM WORKERS " \
                  "GROUP BY Workers.surname, Workers.forename, Workers.idWorker " \
                  "HAVING Workers.idWorker='" + id_leader[1] + "'"

            cursor.execute(sql)

            id_leader = cursor.fetchall()

            insert_query = "INSERT INTO `Projects` (name, startDate, endDate, cost, leader) " \
                           "VALUES ('" + name + "', '" + start_date + "', '" + end_date + "', '" + cost + "', '" + str(id_leader[0]["idWorker"]) + "');"

            cursor.execute(insert_query)

            db.commit()

            return redirect('/Projects')

        elif request.form['action'] == 'Изменить':
            id2 = request.form['id2']
            name2 = request.form['name2']
            cost2 = request.form['cost2']
            start_date2 = request.form['startDate2']
            end_date2 = request.form['endDate2']
            leader2 = request.form['leader2']

            cursor = db.cursor()

            id_leader2 = leader2.split("leader-")

            query = "SELECT Workers.surname, Workers.forename, Workers.idWorker " \
                "FROM WORKERS " \
                "GROUP BY Workers.surname, Workers.forename, Workers.idWorker " \
                "HAVING Workers.idWorker='" + id_leader2[1] + "'"

            cursor.execute(query)

            id_leader2 = cursor.fetchall()

            query = "UPDATE Projects SET " \
                "name ='" + name2 + "', cost='" + cost2 + \
                "', startDate='" + start_date2 + \
                "', endDate='" + end_date2 + "', leader='" + str(id_leader2[0]["idWorker"]) + "' WHERE idProject='" + str(id2) + "'"

            cursor.execute(query)

            db.commit()

            return redirect('/Projects')
    else:
        cursor = db.cursor()

        q = request.args.get('q')

        if q:
            sql = "SELECT Workers.surname, Workers.forename, Projects.idProject, Projects.name, Projects.startDate, " \
                  "Projects.endDate, Projects.cost FROM Workers INNER JOIN Projects ON Workers.idWorker = " \
                  "Projects.leader WHERE ((Workers.surname LIKE '%" + q + "%') OR (Workers.forename LIKE '%" + q + "%')" \
                  " OR (Projects.name LIKE '%" + q + "%')" \
                  " OR (Projects.startDate LIKE '%" + q + "%') OR (Projects.endDate LIKE '%" + q + "%') OR (Projects.cost LIKE '%" + q + "%'))"
        else:
            sql = "SELECT Workers.surname, Workers.forename, Projects.idProject, Projects.name, Projects.startDate, " \
                  "Projects.endDate, Projects.cost, Projects.leader FROM Workers INNER JOIN Projects ON Workers.idWorker = Projects.leader"

        cursor.execute(sql)

        projects_list = cursor.fetchall()

        project_sum = 0

        for project in projects_list:
            project_sum += project['cost']
            project.update({'startDate': project['startDate'].strftime('%d.%m.%Y')})
            project.update({'endDate': project['endDate'].strftime('%d.%m.%Y')})

        cursor.execute("SELECT Workers.surname, Workers.forename, Workers.idWorker FROM Workers WHERE Workers.position = 'Начальник'")

        leaders = cursor.fetchall()

        return render_template('Projects.html', projects_list=projects_list, length=len(projects_list), project_sum=project_sum, leaders=leaders)


@app.route('/Project/delete/<int:project_id>')
def project_delete(project_id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM Executors WHERE (Executors.idProject=' + str(project_id) + ')')
    cursor.execute('DELETE FROM Projects WHERE (Projects.idProject=' + str(project_id) + ')')
    db.commit()
    return redirect('/Projects')


@app.route('/Contracts', methods=['POST', 'GET'])
def contracts():
    if request.method == "POST":
        if request.form['action'] == 'Добавить':
            name = request.form['name']
            client = request.form['client']
            projects_list = request.form.getlist('projects')

            cursor = db.cursor()
            cursor.execute("INSERT INTO `Contracts` (name, client) VALUES ('" + name + "', '" + client + "')")
            cursor.execute("SELECT * FROM Contracts")
            contracts_list = cursor.fetchall()

            last_id = contracts_list[-1]['idContract']

            for project in projects_list:
                insert_query = "INSERT INTO `ContractProject` (idContract, idProject) " \
                               "VALUES ('" + str(last_id) + "', '" + project + "');"
                cursor.execute(insert_query)

            db.commit()

            return redirect('/Contracts')

        elif request.form['action'] == 'Изменить':
            id2 = request.form['idContract2']
            name2 = request.form['name2']
            client2 = request.form['client2']
            projects_list2 = request.form.getlist('projects2')

            cursor = db.cursor()

            query = "UPDATE Contracts SET " \
                "name ='" + name2 + "', client='" + client2 + "' WHERE idContract='" + str(id2) + "'"

            cursor.execute(query)

            cursor.execute('DELETE FROM ContractProject WHERE (ContractProject.idContract=' + str(id2) + ')')

            for project in projects_list2:
                query = "INSERT INTO `ContractProject` (idContract, idProject) " \
                    "VALUES ('" + str(id2) + "', '" + str(project) + "');"
                cursor.execute(query)

            db.commit()

            return redirect('/Contracts')
    else:
        cursor = db.cursor()

        q = request.args.get('q')

        if q:
            sql = "SELECT Contracts.idContract, Min(Projects.startDate) AS MinStartDate, Max(Projects.endDate) AS " \
                  "MaxEndDate, Contracts.name, Contracts.client, Sum(Projects.cost) AS FullCost FROM Projects INNER " \
                  "JOIN (Contracts INNER JOIN ContractProject ON Contracts.IdContract = ContractProject.IdContract) " \
                  "ON Projects.idProject = ContractProject.idProject " \
                  "WHERE ((Contracts.name LIKE '%" + q + "%') OR (Contracts.client LIKE '%" + q + "%')) " \
                  "GROUP BY Contracts.idContract, Contracts.name, Contracts.client"
        else:
            sql = "SELECT Contracts.idContract, Min(Projects.startDate) AS MinStartDate, Max(Projects.endDate) AS " \
                  "MaxEndDate, Contracts.name, Contracts.client, Sum(Projects.cost) AS FullCost FROM Projects INNER " \
                  "JOIN (Contracts INNER JOIN ContractProject ON Contracts.idContract = ContractProject.idContract) " \
                  "ON Projects.idProject = ContractProject.idProject GROUP BY Contracts.idContract, Contracts.name, " \
                  "Contracts.client"

        cursor.execute(sql)

        contracts_list = cursor.fetchall()

        total_sum = 0

        for contract in contracts_list:
            total_sum += contract['FullCost']

        for contract in contracts_list:
            contract.update({'MinStartDate': contract['MinStartDate'].strftime('%d.%m.%Y')})
            contract.update({'MaxEndDate': contract['MaxEndDate'].strftime('%d.%m.%Y')})

        cursor.execute("SELECT * FROM Projects")

        projects_list = cursor.fetchall()

        cursor.execute("SELECT Projects.idProject, Projects.name, Contracts.idContract FROM Contracts INNER JOIN (Projects INNER "
                       "JOIN ContractProject ON Projects.idProject = ContractProject.idProject) "
                       "ON Contracts.idContract = ContractProject.idContract ")

        contract_project_list = cursor.fetchall()

        return render_template('Contracts.html', contracts_list=contracts_list, length=len(contracts_list), total_sum=total_sum,
                               projects_list=projects_list, contract_project_list=contract_project_list)


@app.route('/Contract/delete/<int:contract_id>')
def contract_delete(contract_id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM ContractProject WHERE (ContractProject.idContract=' + str(contract_id) + ')')
    cursor.execute('DELETE FROM Contracts WHERE (Contracts.idContract=' + str(contract_id) + ')')
    db.commit()
    return redirect('/Contracts')


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


if __name__ == '__main__':
    app.run(debug=True)
