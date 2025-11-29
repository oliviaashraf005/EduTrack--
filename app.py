from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json

app = Flask(__name__)

def q_student_table(id):
    try:
        conn = sqlite3.connect("newDEPI.db")
        cursor = conn.cursor()

        

        cursor.execute(f"""
                select st.name , st.s_id, t.t_name, c.ct_name, i.name from Student st
join track_student ts 
on ts.s_id = st.s_id
join Track t 
on ts.t_id = t.t_id
join City c
on c.ct_id = st.ct_id
join student_instructor si
on si.s_id = st.s_id
join Instructor i
on i.i_id = si.i_id
where st.s_id = {id} and i.type = 'tech';

                """)
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        print(f"Error fetching records: {e}")
def q_student_sess(id):
    try:
        conn = sqlite3.connect("newDEPI.db")
        cursor = conn.cursor()

        

        cursor.execute(f"""
                select s.ses_id , s.type, s.date ,i.name, s.state from student_session ss
join student st 
on st.s_id = ss.s_id
join Session s
on ss.ses_id = s.ses_id 
join Instructor i
on s.i_id = i.i_id
where st.s_id = {id} and ss.attendance = 'not taken';

                """)
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        print(f"Error fetching records: {e}")

def Q_student_attend(id):
    try:
        conn = sqlite3.connect("newDEPI.db")
        cursor = conn.cursor()

        

        cursor.execute(f"""
               select count(ss.attendance) from student_session ss
join student st 
on st.s_id = ss.s_id
join Session s
on ss.ses_id = s.ses_id 
where st.s_id = {id} and ss.attendance = 'true';


                """)

        true = cursor.fetchall()[0][0]

        cursor.execute(f"""select count(ss.attendance) from student_session ss
join student st 
on st.s_id = ss.s_id
join Session s
on ss.ses_id = s.ses_id 
where st.s_id = {id} and ss.attendance <> 'not taken';""")
        all = cursor.fetchall()[0][0]

        per =( true / all) * 100
        conn.close()
        return per
    except sqlite3.Error as e:
        print(f"Error fetching records: {e}")
def Q_coor(id):
    try:
        conn = sqlite3.connect("newDEPI.db")
        cursor = conn.cursor()

        

        cursor.execute(f"""
              select co.cor_id , co.name, t.t_name , c.c_name, g.g_name from Coordinator co
join Track t
on co.t_id = t.t_id 
join Company c
on c.c_id = co.c_id
join group_coordinator gc
on gc.cor_id = co.cor_id
join "Group" g
on gc.g_id = g.g_id
where co.cor_id = {id};

                """)

        true = cursor.fetchall()
        conn.close()
       
        return true
    except sqlite3.Error as e:
        print(f"Error fetching records: {e}")
def Q_coor_feed(id):
    try:
        conn = sqlite3.connect("newDEPI.db")
        cursor = conn.cursor()

        

        cursor.execute(f"""
              select st.name , feedback, i.name from Student st
join student_instructor si 
on si.s_id = st.s_id
join Instructor i 
on i.i_id = si.i_id
join student_coordinator sc 
on st.s_id = sc.s_id 
join Coordinator co
on co.cor_id = sc.cor_id
where co.cor_id = {id};

                """)

        true = cursor.fetchall()
        conn.close()
       
        return true
    except sqlite3.Error as e:
        print(f"Error fetching records: {e}")




def Q_coor_attend(id):
    try:
        conn = sqlite3.connect("newDEPI.db")
        cursor = conn.cursor()

        

        cursor.execute(f"""
              
select s.s_id, s.name , g.g_name, cast((cast(count(attendance) as float)/15)*100 as integer)  from Student as s 
join student_session as ss on s.s_id= ss.s_id
join group_student as gs on s.s_id= gs.s_id
join "Group" g
on g.g_id = gs.g_id
join student_coordinator as sc on sc.s_id = s.s_id
where attendance='true' and sc.cor_id={id}
group by s.s_id;
                """)

        all = cursor.fetchall()
        conn.close()

        return all
    except sqlite3.Error as e:
        print(f"Error fetching records: {e}")
def Q_ins_name(id):
    try:
        conn = sqlite3.connect("newDEPI.db")
        cursor = conn.cursor()

        

        cursor.execute(f"""
              
select i.name , i.i_id, r.round_name, i.t_id, t.t_name, c.c_name, i.type from Instructor as i 
join round_instructor as ri on ri.i_id = i.i_id 
join round as r on r.r_id = ri.r_id 
join Track as t on t.t_id = i.t_id 
join company_instructor as ci on ci.i_id = i.i_id
join Company as c on c.c_id = ci.c_id
where i.i_id={id};
                """)

        all = cursor.fetchall()
        conn.close()

        return all
    except sqlite3.Error as e:
        print(f"Error fetching records: {e}")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/ins-log", methods=["GET", "POST"])
def log_inst():
    if request.method == "POST":
        try:
            conn = sqlite3.connect("newDEPI.db")
            cursor = conn.cursor()

            email = request.form["email"]
            passw = request.form["pass"]


            cursor.execute("SELECT cor_id FROM instructor WHERE email = ? AND password = ?", (email, passw))
            result = cursor.fetchall()
            conn.close()

            if result:   # لو فيه طالب
                ins_id = result[0][0]
                return redirect(url_for("instruc", id=ins_id))
            else:
                return render_template("log-ins.html", error="Invalid email or password")
        
        except sqlite3.Error as e:
            print(f"Error fetching records: {e}")
            return render_template("log-ins.html", error="Database error, try again later")

    # لو GET → رجع صفحة تسجيل الدخول
    return render_template("log-ins.html")




@app.route("/com-log")
def log_comp():
    return render_template("log-com.html")


@app.route("/cor-log", methods=["GET", "POST"])
def log_coor():
    if request.method == "POST":
        try:
            conn = sqlite3.connect("newDEPI.db")
            cursor = conn.cursor()

            email = request.form["email"]
            passw = request.form["pass"]


            cursor.execute("SELECT cor_id FROM coordinator WHERE email = ? AND password = ?", (email, passw))
            result = cursor.fetchall()
            conn.close()

            if result:   # لو فيه طالب
                cor_id = result[0][0]
                return redirect(url_for("coord", id=cor_id))
            else:
                return render_template("log-cor.html", error="Invalid email or password")
        
        except sqlite3.Error as e:
            print(f"Error fetching records: {e}")
            return render_template("log-cor.html", error="Database error, try again later")

    # لو GET → رجع صفحة تسجيل الدخول
    return render_template("log-cor.html")


@app.route("/cor-log/coordinator/<int:id>")
def coord(id):
    data = Q_coor(id)[0]
    feed = Q_coor_feed(id)  # [(studentName, feedback, instructor), ...]
    # تحويل tuple list لـ list of dicts
    feed_dict = [{"studentName": s, "feedback": f, "instructor": i} for s, f, i in feed]
    att = Q_coor_attend(id)  # [(id, studentName, group, attendanceRate), ...]

    att_list = [
        {"id": student_id, "name": s, "group": g, "attendanceRate": i}
        for student_id, s, g, i in att
    ]

    return render_template(
        "coor.html",
        data=data,
        feed_json=json.dumps(feed_dict),
        att_json=json.dumps(att_list)
    )
        
    
  
@app.route("/ins-log/instructor/<int:id>")
def instruc(id):
    data = Q_ins_name(id)[0]
    return render_template("instructor.html", data = data)
  


@app.route("/std-log/student/<int:id>")
def student(id):
    data = q_student_table(id)[0]
    id = data[1]
    name = data[0]
    track = data[2]
    city = data[3]
    inst = data[4]
    ses = q_student_sess(id)[0]
    per = int(Q_student_attend(id))

    return render_template("student.html", id = id, name = name,track = track,city = city, inst = inst, per = per, ses = ses)


@app.route("/std-log", methods=["GET", "POST"])
def std_log():
    if request.method == "POST":
        try:
            conn = sqlite3.connect("newDEPI.db")
            cursor = conn.cursor()

            email = request.form["email"]
            passw = request.form["pass"]


            cursor.execute("SELECT s_id FROM student WHERE email = ? AND password = ?", (email, passw))
            result = cursor.fetchall()
            conn.close()

            if result:   # لو فيه طالب
                student_id = result[0][0]
                return redirect(url_for("student", id=student_id))
            else:
                return render_template("log-in.html", error="Invalid email or password")
        
        except sqlite3.Error as e:
            print(f"Error fetching records: {e}")
            return render_template("log-in.html", error="Database error, try again later")

    # لو GET → رجع صفحة تسجيل الدخول
    return render_template("log-in.html")






if __name__ == "__main__":
    app.run(debug=True)
