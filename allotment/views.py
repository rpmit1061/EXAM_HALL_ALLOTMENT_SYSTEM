from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .form import UploadForm, RoomCreateForm
from .models import UploadFile, RoomCreate
import os
import datetime
import psycopg2
from django.views.generic.edit import CreateView

conn = psycopg2.connect("host=localhost dbname=gpcs user=postgres password=12345")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS timetable(
    date character varying,
    br_code character varying,
    sem character varying,
    name_of_subject character varying,
    sub_code character varying,
    paper_code character varying,
    no_of_student character varying,
    remark character varying
) 
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS studentdata(
    enrollment_no character varying,
    first_name character varying,
    father_name character varying,
    mother_name character varying,
    gender character varying,
    category character varying,
    program_name character varying,
    course_code character varying,
    course_name character varying,
    paper_code character varying,
    sub_code character varying,
    status character varying,
    semester character varying,
    paper_type character varying,
    room_status character varying
)
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS allotment(
room_no character varying,
    examdate character varying,
    sub_code character varying,
    enrollment_no character varying
)
""")
conn.commit()
# Create your views here.


def data_sheet_upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        sessionmonth = request.POST['sessionmonth']
        year = request.POST['year']
        if UploadFile.objects.filter(sessionmonth=sessionmonth, year=year).exists():
            resp_body = '<script>alert("For Selected Year and Session file is Already Uploaded");\
                                                            window.location="/allotment/data_sheet_upload"</script>'
            return HttpResponse(resp_body)
        else:
            if form.is_valid():
                form.save()
                filename = 'timefile/' + sessionmonth + '_' + year + '.csv'
                with open(filename, 'r') as f:
                    next(f)
                    cur.copy_from(f, 'timetable', sep=',')
                filename = 'datafile/' + sessionmonth + '_' + year + '.csv'
                with open(filename, 'r') as f:
                    next(f)
                    cur.copy_from(f, 'studentdata', sep=',')
                conn.commit()
            resp_body = '<script>alert("Data Sheet Upload Successfully");\
                                                window.location="/allotment/data_sheet_upload"</script>'
            return HttpResponse(resp_body)
    else:
        username = request.session.get('username')
        if username is None:
            return redirect('/')
        else:
            form = UploadForm()
            alldata = UploadFile.objects.all()
            context = {'form': form, 'alldata': alldata, 'username': username}
            return render(request, 'data_sheet_upload.html', context)


def delete_record(request, ids=None):
    record = get_object_or_404(UploadFile, id=ids)
    if request.method == 'POST':
        file = request.POST['file']
        ttfile = request.POST['ttfile']
        if os.path.isfile(file):
            os.remove(file)
            os.remove(ttfile)
        record.delete()
    resp_body = '<script>alert("Record Deleted Successfully");\
                     window.location="/allotment/data_sheet_upload"</script>'
    return HttpResponse(resp_body)


def room_maintenance(request):
    if request.method == "POST":
        form = RoomCreateForm(request.POST)
        room_no = request.POST['room_no']
        if RoomCreate.objects.filter(room_no=room_no).exists():
            resp_body = '<script>alert("Room Number is already exists. please choose another Room No.");\
                                                window.location="/allotment/room_maintenance"</script>'
            return HttpResponse(resp_body)
        else:
            if form.is_valid():
                form.save()
            resp_body = '<script>alert("Room Created Successfully");\
                                    window.location="/allotment/room_maintenance"</script>'
            return HttpResponse(resp_body)
    else:
        username = request.session.get('username')
        if username is None:
            return redirect('/')
        else:
            form = RoomCreateForm()
            rooms = RoomCreate.objects.all()
            context = {'form': form, 'username': username, 'rooms': rooms}
            return render(request, 'room_maintenance.html', context)


def delete_room(request, idss=None):
    rooms = get_object_or_404(RoomCreate, id=idss)
    if request.method == "POST":
        rooms.delete()
    resp_body = '<script>alert("Room Deleted Successfully");\
                         window.location="/allotment/room_maintenance"</script>'
    return HttpResponse(resp_body)


def allotment(request):
    username = request.session.get('username')
    if username is None:
        return redirect('/')
    else:
        row = None
        examdates = ""
        if request.method == "POST":
            examdate = request.POST['examdate']
            examdates = datetime.datetime.strptime(examdate, '%Y-%m-%d').strftime('%d/%m/%Y')
            if examdates is not None:
                request.session['examdates'] = examdates
            cur.execute(
                "SELECT COUNT(studentdata.enrollment_no),timetable.paper_code FROM studentdata, timetable WHERE "
                "replace(studentdata.paper_code,'''' ,'' )=timetable.paper_code AND studentdata.paper_type='Theory' "
                "AND timetable.date=%s group by timetable.paper_code", [examdates])
            row = cur.fetchall()
        context = {'username': username, 'row': row, 'examdates': examdates}
        return render(request, 'allotment.html', context)


def allotment2(request):
    subject_code = ''
    no_of_student = ''
    username = request.session.get('username')
    if username is None:
        return redirect('/')
    else:
        if request.method == "POST":
            subject_code = request.POST.getlist('subject_code')
            no_of_student = request.POST.getlist('no_of_student')
        sub_code = []
        for item in subject_code:
            sub_code.append(item)
        request.session['sub_code'] = sub_code
        student_get_room = []
        for x in sub_code:
            cur.execute("SELECT count(enrollment_no) FROM studentdata where "
                        "room_status='yes' and paper_type='Theory' "
                        "and replace(paper_code,'''' ,'')=%s", [x])
            student_alloted = cur.fetchall()
            student_get_room.append(student_alloted)
        no_of_std = []
        for i in no_of_student:
            no_of_std.append(i)
        request.session['no_of_std'] = no_of_std
        request.session['student_get_room'] = student_get_room
        data = zip(sub_code, no_of_std, student_get_room)
        cur.execute("""SELECT room_no FROM allotment_roomcreate""")
        row = cur.fetchall()
        request.session['row'] = row
        examdate = request.session.get('examdates')
        context = {'data': data, 'row': row, 'examdate': examdate}
        return render(request, 'allotment2.html', context)


def allotment3(request):
    username = request.session.get('username')
    if username is None:
        return redirect('/')
    else:
        if request.method == "POST":

            allot = request.POST.getlist('allot')
            room_no = request.POST['room_no']
            sub_code = request.session.get('sub_code')
            no_of_std = request.session.get('no_of_std')
            examdate = request.session.get('examdates')
            row = request.session.get('row')
            student_get_room = request.session.get('student_get_room')
            data = zip(sub_code, no_of_std, student_get_room)
            alloted = []
            roll = []
            for i in allot:
                alloted.append(i)
            for i, item in zip(sub_code, alloted):
                cur.execute("SELECT enrollment_no FROM studentdata where room_status='' and paper_type='Theory' "
                            "and replace(paper_code,'''' ,'')=%s limit %s", [i, item])
                rollnumber = cur.fetchall()
                roll.append(rollnumber)

            for i in range(len(roll)):
                m = roll[i]
                for lis in m:
                    cur.execute('INSERT INTO allotment (room_no,sub_code,examdate,enrollment_no)'
                                ' VALUES(%s, %s, %s, %s)', [room_no, sub_code[i], examdate, lis])
                    cur.execute("UPDATE studentdata SET room_status='yes' WHERE replace(paper_code,'''' ,'')=%s "
                                "AND enrollment_no=%s", [sub_code[i], lis])
                    conn.commit()
            global vari
            vari = {'data': data, 'examdate': examdate, 'row': row}
            resp_body = '<script>alert("Room Alloted Successfully");\
                                     window.location="/allotment/allotment3"</script>'
            return HttpResponse(resp_body)
        return render(request, 'allotment2.html', context=vari)


def report(request):
    row = request.session.get('row')

    if request.method == "POST":
        exam_date = request.POST['exam_date']
        exam_date = datetime.datetime.strptime(exam_date, '%Y-%m-%d').strftime('%d/%m/%Y')
        room_no = request.POST['room_no']
        cur.execute("SELECT enrollment_no,sub_code FROM allotment WHERE examdate=%s AND room_no=%s", [exam_date, room_no])
        report_data = cur.fetchall()
        cur.execute("SELECT * FROM allotment_roomcreate where room_no=%s", [room_no])
        room_data = cur.fetchall()
        context = {'row': row, "report_data": report_data, 'room_data': room_data}
        return render(request, 'report.html', context)
    else:
        return render(request, 'report.html', {'row': row})

