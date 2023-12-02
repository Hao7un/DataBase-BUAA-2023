import base64
import os
from datetime import datetime, timedelta

import pymysql
from django.http import HttpResponse
from django.http import JsonResponse
import json
from pymysql.cursors import DictCursor
from settings import DATABASES as db_conf
from settings import IMAGE_PATH
from django.views.decorators.csrf import csrf_exempt


def create_connection():
    return pymysql.connect(host=db_conf["default"]["HOST"],
                           user=db_conf["default"]["USER"],
                           password=db_conf["default"]["PASSWORD"],
                           database=db_conf["default"]["NAME"],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


@csrf_exempt
def register_info(request):  # 传入注册的用户信息，输入到数据库中
    # 用户注册
    assert request.method == "POST"

    request_dict = json.loads(request.body.decode('utf-8'))

    college_id = request_dict["collegeId"]
    user_name = request_dict["userName"]
    password = request_dict["password"]
    email = request_dict["email"]
    telephone = request_dict["telephone"]
    user_type = request_dict["userType"]

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 检查学号是否已经被注册
            cursor.execute("select collegeId from user where collegeId = %s", [college_id])
            users = cursor.fetchall()

            if len(users) != 0:
                resp = {"code": 1,
                        "message": "重复注册"}
                return JsonResponse(resp)

            # 将个人信息插入到数据库中
            cursor.execute(
                'insert into user(collegeId,userName,password,email,telephone,userType) values(%s,%s,%s,%s,%s,%s)',
                [college_id, user_name, password, email, telephone, user_type])
            connection.commit()

    resp = {"code": 0,
            "message": "注册成功"}
    return JsonResponse(resp)


@csrf_exempt
def login_info(request):
    # 用户登陆
    request_dict = json.loads(request.body.decode('utf-8'))
    college_id = request_dict["collegeId"]
    password = request_dict["password"]
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("select userId,userType,userName,password from user where collegeId = %s", [college_id])
            result = cursor.fetchall()
            connection.commit()
            # print(len(result))
            if len(result) == 0:
                resp = {
                    "code": 1,
                    "message": "用户不存在"
                }
                return JsonResponse(resp)
            elif len(result) == 1:
                correct_password = result[0]['password']
                userId = str(result[0]['userId'])
                userType = result[0]['userType']
                userName = result[0]['userName']
                if correct_password == password:
                    resp = {
                        "code": 0,
                        "message": "登陆成功",
                        "userId": userId,
                        "userType": userType,
                        "userName": userName
                    }
                    return JsonResponse(resp)
                else:
                    resp = {
                        "code": 2,
                        "message": "密码错误"
                    }
                    return JsonResponse(resp)


@csrf_exempt
def update_user_info(request):
    # 确保这是一个 POST 请求
    if request.method != 'POST':
        return JsonResponse({"code": 1, "message": "无效请求"})

    # 解析请求体中的 JSON 数据
    request_dict = json.loads(request.body.decode('utf-8'))

    # 获取要更新的用户信息
    userId = request_dict.get("userId")
    new_email = request_dict.get("email")
    new_telephone = request_dict.get("telephone")
    new_intro = request_dict.get("userIntro")

    # 创建数据库连接
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 更新数据库中的用户信息
            update_statement = """
                UPDATE user
                SET email = %s, telephone = %s, userIntro = %s
                WHERE userId = %s
            """
            cursor.execute(update_statement, [new_email, new_telephone, new_intro, int(userId)])
            connection.commit()

    # 返回成功响应
    return JsonResponse({"code": 0, "message": "用户信息更新成功"})


@csrf_exempt
def change_password(request):
    # 确保这是一个 POST 请求
    if request.method != 'POST':
        return JsonResponse({"code": 1, "message": "无效请求"})

    # 解析请求体中的 JSON 数据
    request_dict = json.loads(request.body.decode('utf-8'))

    # 获取学号和新旧密码
    userId = request_dict.get("userId")
    new_password = request_dict.get("newPassword")

    # 创建数据库连接
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 更新密码
            update_statement = "UPDATE user SET password = %s WHERE userId = %s"
            cursor.execute(update_statement, [new_password, userId])
            connection.commit()

    # 返回成功响应
    return JsonResponse({"code": 0, "message": "密码已成功更新"})


@csrf_exempt
def get_user_info(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    userId = request_dict.get("userId")

    if not userId:
        return JsonResponse({"error": "Missing userId parameter"})

    # 连接数据库
    connection = create_connection()
    user_info = None
    with connection:
        with connection.cursor(DictCursor) as cursor:
            cursor.execute(
                'SELECT collegeId,userName,email,telephone,password,userIntro FROM user WHERE userId = %s',
                [userId]
            )
            user_info = cursor.fetchone()

            cursor.execute(
                'SELECT totalHours FROM user_volunteerhours WHERE userId = %s',
                [userId]
            )
            result = cursor.fetchone()
            if result is None:
                volunteer_time = 0
            else:
                volunteer_time = result.get('totalHours')

            connection.commit()

    # 检查是否找到了指定的用户
    if not user_info:
        return JsonResponse({"error": "User not found"})

    # 返回用户信息
    return JsonResponse({"code": 0,
                         "message": "获取信息成功",
                         "telephone": user_info.get('telephone'),
                         "email": user_info.get('email'),
                         "volunteerTime": volunteer_time,
                         "userIntro": user_info.get('userIntro')
                         })


@csrf_exempt
def user_get_message(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")

    connection = create_connection()
    with connection:
        with connection.cursor(DictCursor) as cursor:
            cursor.execute(
                'SELECT messageId,messageTime,messageTitle,messageContent, messageIsRead FROM message WHERE receiverId = %s',
                [user_id])
            messages = cursor.fetchall()
            message_list = []
            for message in messages:
                message_id = message['messageId']
                message_time = message['messageTime']
                message_title = message['messageTitle']
                message_content = message['messageContent']
                message_is_read = message['messageIsRead']

                if message_is_read == 'True':
                    message_is_read = True
                else:
                    message_is_read = False

                message_list.append({
                    'id': message_id,
                    'title': message_title,
                    'time': message_time.strftime("%Y-%m-%d %H:%M"),
                    'content': message_content,
                    'isRead': message_is_read
                })
        connection.commit()

    return JsonResponse({
        'code': 0,
        'messages': message_list
    })


@csrf_exempt
def user_read_message(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    message_id = request_dict.get("messageId")
    connection = create_connection()
    with connection:
        with connection.cursor(DictCursor) as cursor:
            cursor.execute('UPDATE message SET messageIsRead = %s WHERE messageId = %s', ['True', message_id])
            connection.commit()

    return JsonResponse({
        'code': 0,
        'message': '信息状态修改成功'
    })


def system_send_message(request, user_ids):
    request_dict = json.loads(request.body.decode('utf-8'))
    message_title = request_dict.get('message').get('title')
    message_content = request_dict.get('message').get('content')
    cur_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            for user_id in user_ids:
                cursor.execute('insert into message(messageTime,messageTitle,messageContent,messageIsRead,receiverId) '
                               'values (%s,%s,%s,%s,%s)', [cur_time, message_title, message_content, 'False', user_id])
            connection.commit()

    return 'Successfully Sending Messages'


@csrf_exempt
def upload_user_avatar(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")
    img = request.FILES["file"]

    # 文件名
    img_name = img.name.split('/')[-1]
    img_name = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S") + img_name

    # 存储的文件夹
    img_dir = IMAGE_PATH + 'userAvatar/' + user_id
    img_path = img_dir + '/' + img_name
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    with open(img_path, 'wb+') as destination:
        for chunk in img.chunks():
            destination.write(chunk)

    with open(img_dir + '/' + img_name, "rb") as f:
        img = f.read()

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'insert into image(imageName,imageURL) values (%s,%s)',
                [img_name, img]
            )

            cursor.execute('SELECT LAST_INSERT_ID()')
            image_id = cursor.fetchone()[0]

            # 更新用户的 avatarId 字段
            cursor.execute(
                'UPDATE user SET avatarId = %s WHERE userId = %s',
                [image_id, user_id]
            )
            connection.commit()

    return HttpResponse(None)


@csrf_exempt
def get_user_avatar(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 查询用户的 avatarId
            cursor.execute("SELECT avatarId FROM user WHERE userId = %s", [user_id])
            result = cursor.fetchone()

            # 没有上传头像
            if result['avatarId'] is None:
                return HttpResponse('')

            avatar_id = result['avatarId']

            # 查询头像的详细信息
            cursor.execute("SELECT imageURL FROM image WHERE imageId = %s", [avatar_id])
            avatar_info = cursor.fetchone()

            image_url = avatar_info['imageURL']
            img = base64.b64encode(image_url)

            # 返回头像信息
            return HttpResponse(img, content_type='image/jpeg')
