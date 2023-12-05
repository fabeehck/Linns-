from functools import wraps
from flask import Flask, render_template, request, url_for, redirect, flash, session

from flaskext.mysql import MySQL
wrong = Flask(__name__)
wrong.secret_key = "LKGJDSD^S%D^&S*D)S_(DIUOHSBXFSDRS$^$&%*^*())"


wrong.config['MYSQL_DATABASE_HOST'] = 'localhost'
wrong.config['MYSQL_DATABASE_USER'] = 'root'
wrong.config['MYSQL_DATABASE_PASSWORD'] = 'fabee'
wrong.config['MYSQL_DATABASE_DB'] = 'linns'


MySQL_object = MySQL()
MySQL_object.init_app(wrong)


# decorator to check wheather the user is logined or not.


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function


@wrong.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


@wrong.route("/")
def Home():
    return render_template('home.html')


@wrong.route("/admin")
def admin_home():
    return render_template('admin_home.html')


@wrong.route("/teachers")
def taecherss():
    return render_template('.html')


@wrong.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        data = request.form
        connection = MySQL_object.connect()
        cursor = connection.cursor()

        print(data)

        cursor.execute("select * from login where username=%s and password=%s",
                       (data["username"], data["password"]))
        data = cursor.fetchone()

        print(data)
        if data is None:
            return "invalid username or password"
        else:
            session["username"] = data[1]
            session['type'] = data[3]
            session['reg_id'] = data[4]

            if data[3] == "admin":
                return render_template('admin_home.html')
            elif data[3] == "teacher":
                return "teacher login successfull"
            elif data[3] == "student":
                return "student login succesfull"
            else:
                return "invalid attempt"


@wrong.route("/hyy", methods=['GET', 'POST'])
@login_required
def department():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()

        cursor.execute("select * from `department`")
        dept = cursor.fetchall()
        connection.close()
        return render_template('department.html', departments=dept)

    elif request.method == "POST":
        data = request.form
        print(data)
        connection = MySQL_object.connect()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO `department`(`department`)VALUES(%s);", (request.form['department']))

        connection.commit()
        flash("Course added successfully")
        cursor.close()
        connection.close()
        return redirect(url_for("department"))


@wrong.route("/course", methods=['GET', 'POST'])
def course():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("select * from `department`")
        fabee = cursor.fetchall()

        connection.close()
        return render_template('course.html', datasss=fabee)

    elif request.method == "POST":
        data = request.form
        print(data)
        cou_cou = []
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("select * from `department`")
        fabee = cursor.fetchall()
        if "course" in request.form:
            cursor.execute("INSERT INTO `course`(`department_id`,`course`)VALUES(%s,%s);",
                           (data['department'], data['course']))
            connection.commit()
        flash("Course added successfully")
        if "corse_idd" in request.form:
            cursor.execute(
                "select * from course where department_id=%s", request.form['corse_idd'])
            cou_cou = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('course.html', data=cou_cou, datasss=fabee)


@wrong.route("/batc", methods=['GET', 'POST'])
def batch():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("select * from `department`")
        dept_course = cursor.fetchall()
        connection.close()
        return render_template('batch.html', datas=dept_course)

    elif request.method == "POST":
        print(request.form)
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("select * from `department`")
        dept_course = cursor.fetchall()

        cursor.execute("select * from course where department_id=%s",
                       request.form['department'])
        dept_dept = cursor.fetchall()
        if "course_idd" in request.form:

            cursor.execute("select * from batch where course_id=%s",
                           request.form['course_idd'])
            deptab = cursor.fetchall()
            return render_template('batch.html', depts=dept_dept, datas=dept_course, dapts=deptab)
        cursor.close()
        connection.close()
        return render_template('batch.html', depts=dept_dept, datas=dept_course)


@wrong.route("/batch", methods=['GET', 'POST'])
def batc():
    if request.method == 'GET':
        print(request.form)
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("select * from `department`")
        dept_course = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('batch.html', datas=dept_course)
    elif request.method == "POST":
        print(request.form)
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO `batch`(`course_id`,`batch`)VALUES(%s,%s);",
                       (request.form['course'], request.form['batch']))
        connection.commit()
        cursor.close()
        connection.close()
        return render_template('batch.html')


@wrong.route("/sem", methods=['GET', 'POST'])
def semest():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("select * from `department`")
        dep = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('sem.html', dep_slt=dep)

    else:
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        idsm = []
        battch_sort = []
        print(request.form)
        cursor.execute("select * from course where department_id=%s",
                       request.form['department_id'])
        crs = cursor.fetchall()
        if "course_id" in request.form:
            cursor.execute("select * from batch where course_id=%s",
                           request.form['course_id'])
            idsm = cursor.fetchall()
        if "batch_id" in request.form:
            if request.form['batch_id'] != 'Select batch':
                cursor.execute(
                    "select * from semester where batch_id=%s", request.form['batch_id'])
                battch_sort = cursor.fetchall()
        if "table_datas" not in request.form:
            if "batch_id" in request.form:
                if request.form['batch_id'] != '' and request.form['batch_id'] != 'Select batch':
                    cursor.execute("INSERT INTO `semester`(`batch_id`,`semester`)VALUES(%s,%s);",
                                   (request.form['batch_id'], request.form['semester']))
                    connection.commit()
                    flash("Course added successfully")
        else:
            flash("Please select a batch")

        cursor.close()
        connection.close()
        return render_template('sem.html', sem_crs=crs, btchs_sm=idsm, semesterss=battch_sort)


@wrong.route("/sub", methods=['GET', 'POST'])
def subject():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("select * from `department`")
        deptt = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('subject.html', dep_sub=deptt)

    else:
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        idsubb = []
        idsmm = []
        seme_sub = []
        print(request.form)
        cursor.execute("select * from course where department_id=%s",
                       request.form['department_id'])
        crss = cursor.fetchall()
        if "course_id" in request.form:
            cursor.execute("select * from batch where course_id=%s",
                           request.form['course_id'])
            idsubb = cursor.fetchall()
        if "batch_id" in request.form:
            cursor.execute(
                "select * from semester where batch_id=%s", request.form['batch_id'])
            idsmm = cursor.fetchall()
        if "semester_id" in request.form:
            cursor.execute(
                "select * from subject where semester_id=%s", request.form['semester_id'])
            seme_sub = cursor.fetchall()
        if "table_data" not in request.form:
            if "semester_id" in request.form:
                if request.form['semester_id'] != '' and request.form['semester_id'] != 'Select semester':
                    cursor.execute("INSERT INTO `subject`(`semester_id`,`subject`)VALUES(%s,%s);",
                                   (request.form['semester_id'], request.form['subject']))
                    connection.commit()
                    flash("Course added successfully")
            else:
                flash("Please select a semester")
        cursor.close()
        connection.close()
        return render_template('subject.html', sub_crs=crss, smsub=idsubb, sub_seme=idsmm, subjucts=seme_sub)


@wrong.route("/addteach", methods=['GET', 'POST'])
def addteachh():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("select * from `department`")
        deptte = cursor.fetchall()
        cursor.execute("select * from `student_batch_maping`")
        map = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('add_teacher.html', tea_dpt=deptte, maping=map)

    else:
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cou_tea = []
        bat_tea = []
        sub_tea = []
        teaa = []
        print(request.form)
        cursor.execute("select * from `department`")
        deptte = cursor.fetchall()
        cursor.execute("select * from registration")
        teaa = cursor.fetchall()
        cursor.execute("select * from course where department_id=%s",
                       request.form['department_id'])
        tea_depts = cursor.fetchall()
        if "course_id" in request.form:
            cursor.execute("select * from batch where course_id=%s",
                           request.form['course_id'])
            cou_tea = cursor.fetchall()
        if "batch_id" in request.form:
            cursor.execute(
                "select * from semester where batch_id=%s", request.form['batch_id'])
            bat_tea = cursor.fetchall()
        if "semester_id" in request.form:
            cursor.execute(
                "select * from subject where semester_id=%s", request.form['semester_id'])
            sub_tea = cursor.fetchall()
        if "teacher_data" not in request.form:
            if "teacher_id" in request.form:
                if request.form["teacher_id"] != '' and request.form['teacher_id'] != 'Select teachers':
                    cursor.execute(
                        "INSERT INTO `addingteacher_mapping`(`subject_id`,`teacher_id`)VALUES(%s,%s);", (request.form['subject_id'], request.form['teacher_id']))
                    connection.commit()

        cursor.close()
        connection.close()
        return render_template('add_teacher.html', depts_tea=tea_depts, tea_cou=cou_tea, tea_bat=bat_tea, tea_sub=sub_tea, teachers=teaa, tea_dpt=deptte)


@wrong.route("/teach", methods=['GET', 'POST'])
def teacher():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("select * from `course`")
        dept_teach = cursor.fetchall()
        cursor.execute("select * from `registration`")
        teac = cursor.fetchall()

        connection.close()
        return render_template('teacher.html', teach=dept_teach, teaching=teac)

    elif request.method == "POST":
        data = request.form
        print(data)
        connection = MySQL_object.connect()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO `linns`.`registration`(`name`,`email`,`phone`)VALUES(%s,%s,%s);",
                       (data["name"], data["email"], data["phone"]))
        connection.commit()

        cursor.execute("INSERT INTO `linns`.`login`(`username`,`password`,`type`,`reg_id`)VALUES(%s,%s,%s,%s);",
                       (data["username"], data["password"], 'teacher', cursor.lastrowid))
        connection.commit()

        flash("Teacher added successfully")
        cursor.close()
        connection.close()
        return redirect(url_for("teacher"))


@wrong.route("/exam", methods=['GET', 'POST'])
def examination():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("select * from `subject`")
        dept_sub = cursor.fetchall()
        cursor.execute("select * from `subject`")
        sosub = cursor.fetchall()
        connection.close()
        return render_template('exam.html', sub=dept_sub, subsort=sosub)

    elif request.method == "POST":
        data = request.form
        print(data)
        connection = MySQL_object.connect()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO `exam`(`subject`)VALUES(%s);",
                       (data['subject']))
        connection.commit()
        flash("Course added successfully")
        cursor.close()
        connection.close()
        return redirect(url_for("examination"))


@wrong.route("/add", methods=['GET', 'POST'])
def student():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("select * from `department`")
        dept_stu = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('add_student.html', stu_crs=dept_stu)

    else:
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        stu_cou = []

        print(request.form)
        cursor.execute("select * from course where department_id=%s",
                       request.form['department_id'])
        crs_stu = cursor.fetchall()
        if "course_id" in request.form:
            cursor.execute("select * from batch where course_id=%s",
                           request.form['course_id'])
            stu_cou = cursor.fetchall()

        if "batchs_id" in request.form:
            if request.form['batchs_id'] != 'Select batches':
                cursor.execute("INSERT INTO `linns`.`registration`(`name`,`email`,`phone`)VALUES(%s,%s,%s);", (
                    request.form["name"], request.form["email"], request.form["phone"]))
                connection.commit()
                reg_id = cursor.lastrowid
                cursor.execute("INSERT INTO `linns`.`login`(`username`,`password`,`type`,`reg_id`)VALUES(%s,%s,%s,%s);", (
                    request.form["phone"], request.form["phone"], "student", reg_id))
                connection.commit()
                cursor.execute("update `linns`.`registration` set reg_no=%s where id=%s", (
                    f"REG-{reg_id}", reg_id))
                connection.commit()

                cursor.execute("INSERT INTO `linns`.`student_batch_maping`(`batchs_id`,`regs_id`)VALUES(%s,%s);", (
                    request.form["batchs_id"], reg_id))
                connection.commit()
                flash("student added successfully")
        else:
            flash("Please select a batch")
        cursor.close()
        connection.close()
        return render_template('add_student.html', cou_stu=crs_stu, bat_stu=stu_cou)


@wrong.route("/update_dept", methods=['GET', 'POST'])
def update_dept():
    if request.method == "POST":
        print(request.form)
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        if request.form["action"] == "Update":
            cursor.execute("update department set department=%s where id=%s",
                           (request.form['departement'], request.form['id']))
        if request.form["action"] == "delete":
            cursor.execute("delete from department where id=%s",
                           request.form['id'])
        connection.commit()
        return redirect(url_for("department"))


@wrong.route("/update_cou", methods=['GET', 'POST'])
def update_course():
    if request.method == "POST":
        print(request.form)
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        if request.form["action"] == "Update":
            cursor.execute("update course set course=%s where id=%s",
                           (request.form['course'], request.form['id']))
        if request.form["action"] == "delete":
            cursor.execute("delete from course where id=%s",
                           request.form['id'])
        connection.commit()
        return redirect(url_for("course"))


@wrong.route("/update_sub", methods=['GET', 'POST'])
def update_subjuct():
    if request.method == "POST":
        print(request.form)
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        if request.form["action"] == "Update":
            cursor.execute("update subject set subject=%s where id=%s",
                           (request.form['subject'], request.form['id']))
        if request.form["action"] == "delete":
            cursor.execute("delete from subject where id=%s",
                           request.form['id'])
        connection.commit()
        return redirect(url_for("subject"))


@wrong.route("/update_sem", methods=['GET', 'POST'])
def update_semster():
    if request.method == "POST":
        print(request.form)
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        if request.form["action"] == "Update":
            cursor.execute("update semester set semester=%s where id=%s",
                           (request.form['semester'], request.form['id']))
        if request.form["action"] == "delete":
            cursor.execute("delete from semester where id=%s",
                           request.form['id'])
        connection.commit()
        return redirect(url_for("semest"))


# hostal management

@wrong.route("/hostel", methods=['GET', 'POST'])
def hostel():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()

        cursor.execute("select * from `type`")
        typee = cursor.fetchall()
        connection.close()
        return render_template('type.html', types=typee)

    elif request.method == "POST":
        data = request.form
        print(data)
        connection = MySQL_object.connect()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO `type`(`type`)VALUES(%s);", (request.form['type']))

        connection.commit()
        flash("Course added successfully")
        cursor.close()
        connection.close()
        return redirect(url_for("hostel"))


@wrong.route("/update_type", methods=['GET', 'POST'])
def update_type():
    if request.method == "POST":
        print(request.form)
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        if request.form["action"] == "Update":
            cursor.execute("update type set type=%s where id=%s",
                           (request.form['type'], request.form['id']))
        if request.form["action"] == "delete":
            cursor.execute("delete from type where id=%s",
                           request.form['id'])
        connection.commit()
        return redirect(url_for("hostel"))


@wrong.route("/floor", methods=['GET', 'POST'])
def floor():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()

        cursor.execute("select * from `floor`")
        floorr = cursor.fetchall()
        connection.close()
        return render_template('floor.html', floores=floorr)

    elif request.method == "POST":
        data = request.form
        print(data)
        connection = MySQL_object.connect()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO `floor`(`floor`)VALUES(%s);", (request.form['floor']))

        connection.commit()
        flash("floor added successfully")
        cursor.close()
        connection.close()
        return redirect(url_for("floor"))


@wrong.route("/update_floor", methods=['GET', 'POST'])
def update_floor():
    if request.method == "POST":
        print(request.form)
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        if request.form["action"] == "Update":
            cursor.execute("update floor set floor=%s where id=%s",
                           (request.form['floor'], request.form['id']))
        if request.form["action"] == "delete":
            cursor.execute("delete from floor where id=%s",
                           request.form['id'])
        connection.commit()
        return redirect(url_for("floor"))


@wrong.route("/room", methods=['GET', 'POST'])
def roomss():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("select * from `type`")
        types = cursor.fetchall()
        cursor.execute("select * from floor")
        floorr = cursor.fetchall()
        cursor.execute("select * from rooms")
        ro_om = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('room.html', typess=types, flooress=floorr, roo_m=ro_om)

    else:
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        floorr = []
        battch_sort = []
        print(request.form)

        cursor.execute("select * from floor")
        floorr = cursor.fetchall()

        cursor.execute("INSERT INTO `rooms`(`type_id`,`floor_id`,`rooms`)VALUES(%s,%s,%s);",
                       (request.form['type_id'], request.form['floor_id'], request.form['rooms']))
        connection.commit()
        flash("Course added successfully")

        cursor.close()
        connection.close()
        return render_template('room.html', flooress=floorr, semesterss=battch_sort)


@wrong.route("/nobed", methods=['GET', 'POST'])
def noofbed():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute("select * from rooms")
        bedes = cursor.fetchall()
        cursor.execute(
            "select * from rooms r, no_beds n where r.id=n.rooms_id")
        nobed = cursor.fetchall()

        cursor.close()
        connection.close()
        return render_template('no_of_beds.html', bedess=bedes, bedno=nobed)

    else:
        connection = MySQL_object.connect()
        cursor = connection.cursor()

        print(request.form)
        bed_names = request.form["name_bed"].split(",")
        for item in bed_names:
            cursor.execute("INSERT INTO `no_beds`(`rooms_id`,`no_beds`,`name_bed`)VALUES(%s,%s,%s);",
                           (request.form['rooms_id'], request.form['no_beds'], item))
            connection.commit()
        flash("Course added successfully")

        cursor.close()
        connection.close()
        return render_template('no_of_beds.html')


@wrong.route("/bed", methods=['GET', 'POST'])
def bedss():
    print(request.method)
    if request.method == 'GET':
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        cursor.execute(
            "select * from registration r,login l where l.type='student' and r.id=l.reg_id")
        stu_bed = cursor.fetchall()
        cursor.execute("select * from rooms")
        nabed = cursor.fetchall()
        cursor.execute("select * from no_beds")
        noofbed = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('beds.html', bed_stu=stu_bed, bedna=nabed,bedofno=noofbed)

    else:
        connection = MySQL_object.connect()
        cursor = connection.cursor()
        stu_bed = []

        print(request.form)

        cursor.execute("select * from registration r,login l where l.type='student' and r.id=l.reg_id")

        stu_bed = cursor.fetchall()

        cursor.execute("select * from rooms")
        nabed = cursor.fetchall()

        cursor.execute("select * from no_beds")
        noofbed = cursor.fetchall()

        cursor.execute("INSERT INTO `bed`(`room_id`,`students_id`,`bed_no`,`date_from`,`date_to`)VALUES(%s,%s,%s,%s,%s);",
                       (request.form['room_id'], request.form['students_id'], request.form['bed_no'], request.form['date_from'], request.form['date_to']))
        connection.commit()
        flash("Course added successfully")

        cursor.close()
        connection.close()
        return render_template('beds.html', bed_stu=stu_bed, bedna=nabed,bedofno=noofbed)


if __name__ == '__main__':
    wrong.run(debug=True)
