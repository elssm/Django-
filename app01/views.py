from urllib import request
import json
from django.shortcuts import render,redirect,HttpResponse
import pymysql
def classes(request):
    #去请求的cookie中找凭证
    #tk = request.COOKIES.get('ticket')
    tk = request.get_signed_cookie('ticket',salt='jjjjjjj')
    if not tk:
        return redirect('/login/')
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    effect_row = cursor.execute("select id,title from class")
    class_list = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    return render(request,'classes.html',{'class_list':class_list})

def add_class(request):
    if request.method == 'GET':
        return render(request,'add_class.html')
    else:
        v = request.POST.get('title')
        if len(v) > 0:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
            # 创建游标
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute("insert into class(title) values(%s)",[v,])
            conn.commit()
            cursor.close()
            # 关闭连接
            conn.close()
            return redirect('/classes/')
        else:
            return render(request, 'add_class.html',{'msg':'班级名称不能为空'})

def del_class(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from class where id=%s", [nid, ])
    conn.commit()
    cursor.close()
    # 关闭连接
    conn.close()
    return redirect('/classes/')

def edit_class(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class where id = %s", [nid, ])
        result = cursor.fetchone()
        cursor.close()
        # 关闭连接
        conn.close()
        return render(request,'edit_class.html',{'result':result})
    else:
        nid = request.GET.get('nid') #这块死活拿不到数据
        #nid = request.POST.get('id')
        title = request.POST.get('title')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update class set title=%s where id = %s",[title,nid,])
        conn.commit()
        cursor.close()
        # 关闭连接
        conn.close()
        print(nid)
        return redirect('/classes/')

def students(request):
    '''
    学生列表
    :param request: 封装请求相关所有信息
    :return:
    '''
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select student.id,student.name,student.class_id,class.title from student LEFT JOIN class on student.class_id =class.id")
    student_list = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,title from class",[])
    class_list = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    return render(request,'students.html',{'student_list':student_list,'class_list':class_list})

def add_student(request):
    if request.method =="GET":
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class")
        class_list = cursor.fetchall()
        cursor.close()
        # 关闭连接
        conn.close()
        return render(request, 'add_student.html',{'class_list':class_list})
    else:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert into student(name,class_id) values(%s,%s)",[name,class_id,])
        conn.commit()
        cursor.close()
        # 关闭连接
        conn.close()
        return redirect('/students/')

def del_student(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from student where id=%s", [nid,])
    conn.commit()
    cursor.close()
    # 关闭连接
    conn.close()
    return redirect('/students/')

def edit_student(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        effect_row = cursor.execute("select id,title from class")
        class_list = cursor.fetchall()
        cursor.close()
        # 关闭连接
        conn.close()
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,name,class_id from student where id = %s", [nid, ])
        current_student_info = cursor.fetchone()
        cursor.close()
        # 关闭连接
        conn.close()
        return render(request,'edit_student.html',{'class_list':class_list,'current_student_info':current_student_info})
    else:
        nid = request.POST.get('id')
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update student set name=%s,class_id =%s where id = %s", [name, class_id, nid,])
        conn.commit()
        cursor.close()
        # 关闭连接
        conn.close()
        return redirect('/students/')



###########################  对话框  ############################

def modal_add_class(request):
    title = request.POST.get('title')
    if len(title) > 0:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert into class(title) values(%s)", [title, ])
        conn.commit()
        cursor.close()
        # 关闭连接
        conn.close()
        #return redirect('/classes/')
        return HttpResponse('ok')
    else:
        #页面不要刷新，提示错误信息
        return HttpResponse('班级标题不能为空')


def modal_edit_class(request):
    ret = {'status':True,'message':None}
    try:
        nid  =request.POST.get('nid')
        content = request.POST.get('content')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update class set title=%s where id = %s", [content,nid, ])
        conn.commit()
        cursor.close()
        # 关闭连接
        conn.close()
    except Exception as e:
        ret['status'] = False
        ret['message'] = '处理异常'

    return HttpResponse(json.dumps(ret))

def modal_add_student(request):
    ret = {'status':True,'message':None}
    try:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert into student(name,class_id) values(%s,%s)", [name, class_id, ])
        conn.commit()
        cursor.close()
        # 关闭连接
        conn.close()
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)

    return HttpResponse(json.dumps(ret))

def modal_edit_student(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update student set name=%s,class_id=%s where id = %s", [name, class_id,nid, ])
        conn.commit()
        cursor.close()
        # 关闭连接
        conn.close()
        print(nid,name,class_id)
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)

    return HttpResponse(json.dumps(ret))


#对多对，以老师表展示
def teachers(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("""
    select teacher.id as tid,teacher.name,class.title from teacher
    LEFT JOIN teacher2class on teacher.id = teacher2class.teacher_id
    LEFT JOIN class on class.id = teacher2class.class_id;

    """,[])
    teacher_list = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    result = {}
    for row in teacher_list:
        tid = row['tid']
        if tid in result:
            result[tid]['titles'].append(row['title'])
        else:
            result[tid] = {'tid':row['tid'],'name':row['name'],'titles':[row['title'],]}
    return render(request,'teacher.html',{'teacher_list':result.values()})

def add_teacher(request):
    if request.method == 'GET':
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class", [])
        class_list=cursor.fetchall()
        cursor.close()
        # 关闭连接
        conn.close()
        return render(request,'add_teacher.html',{'class_list':class_list})
    else:
        name = request.POST.get('name')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        #老师表中添加一条数据
        cursor.execute("insert into teacher(name) values(%s)", [name,])
        conn.commit()
        last_row_id = cursor.lastrowid
        teacher_id = last_row_id
        #老师和班级关系表中插入数据
        #获取当前添加的老师id
        cursor.close()
        # 关闭连接
        conn.close()
        class_ids = request.POST.getlist('class_ids')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        for cls_id in class_ids:
            # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
            # # 创建游标
            # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            # 老师表中添加一条数据
            cursor.execute("insert into teacher2class(teacher_id,class_id) values(%s,%s)", [teacher_id,cls_id ])
            conn.commit()
        cursor.close()
        # 关闭连接
        conn.close()
        print(name,class_ids)
        return redirect('/teachers/')

def edit_teacher(request):
    if request.method =='GET':
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,name from teacher where id = %s", [nid,])
        teacher_info = cursor.fetchone()
        cursor.execute("select class_id from teacher2class where teacher_id = %s", [nid, ])
        class_id_list = cursor.fetchall()
        cursor.execute("select id,title from class", [])
        class_list = cursor.fetchall()
        cursor.close()
        # 关闭连接
        conn.close()
        temp=[]
        for i in class_id_list:
            temp.append(i['class_id'])

        print(teacher_info)
        print(class_id_list)
        print(class_list)
        #return HttpResponse('.....')
        return render(request,'edit_teacher.html',{'teacher_info':teacher_info,'class_id_list':temp,'class_list':class_list,})
    else:
        nid = request.POST.get('id')
        name = request.POST.get('name')
        class_ids = request.POST.getlist('class_ids')
        #更新老师表
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update teacher set name=%s where id = %s", [name,nid ])
        conn.commit()
        cursor.close()
        # 关闭连接
        conn.close()
        #更新老师和班级关系表
        #先把当前老师和班级的对应关系删除，然后再添加
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("delete from teacher2class where teacher_id = %s", [nid,])
        conn.commit()
        cursor.close()
        # 关闭连接
        conn.close()
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标

        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        for cls_id in class_ids:
            # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
            # # 创建游标
            # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            # 老师表中添加一条数据
            cursor.execute("insert into teacher2class(teacher_id,class_id) values(%s,%s)", [nid, cls_id])
            conn.commit()
        cursor.close()
        # 关闭连接
        conn.close()
        return redirect('/teachers/')


def get_all_class(request):
    import time
    #time.sleep(5)
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,title from class", [])
    class_list = cursor.fetchall()
    cursor.close()
    # 关闭连接
    conn.close()
    return HttpResponse(json.dumps(class_list))

def modal_add_teacher(request):
    ret = {'status':True,'message':None}
    try:
        name = request.POST.get('name')
        class_id_list = request.POST.getlist('class_id_list')
        print(name,class_id_list)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        #老师表中添加一条数据
        cursor.execute("insert into teacher(name) values(%s)", [name,])
        last_row_id = cursor.lastrowid
        teacher_id = last_row_id
        conn.commit()
        for cls_id in class_id_list:
            # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='sudo520926cmd', db='djangodb')
            # # 创建游标
            # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            # 老师表中添加一条数据
            cursor.execute("insert into teacher2class(teacher_id,class_id) values(%s,%s)", [teacher_id, cls_id])
            conn.commit()
        cursor.close()
        # 关闭连接
        conn.close()
    except Exception as e:
        ret['status'] = False
        ret['message'] = '处理失败'
    return  HttpResponse(json.dumps(ret))

def layout(request):
    return render(request,'layout.html')

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        if user == 'elssm' and pwd == '123':
            obj = redirect('/classes/')
            obj.set_signed_cookie('ticket','123123',salt='jjjjjjj')
            return obj
        else:
            return render(request,'login.html')
