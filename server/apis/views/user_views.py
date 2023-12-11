import base64
import os
from datetime import datetime, timedelta

import pymysql
from django.http import HttpResponse
from settings import DATABASES as db_conf
from settings import IMAGE_PATH
from django.http import JsonResponse
import json
from pymysql.cursors import DictCursor
from django.views.decorators.csrf import csrf_exempt


def create_connection():
    return pymysql.connect(host=db_conf["default"]["HOST"],
                           user=db_conf["default"]["USER"],
                           password=db_conf["default"]["PASSWORD"],
                           database=db_conf["default"]["NAME"],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


@csrf_exempt
def register_info(request):
    request_dict = json.loads(request.body.decode('utf-8'))

    # 准备存储过程的参数
    params = [
        request_dict["collegeId"],
        request_dict["userName"],
        request_dict["password"],
        request_dict["email"],
        request_dict["telephone"],
        request_dict["userType"]
    ]

    connection = create_connection()
    # 调用存储过程并处理结果
    with connection:
        with connection.cursor() as cursor:
            cursor.callproc('register_info', params + [0])  # 添加一个额外的参数用于输出结果
            cursor.execute('SELECT @register_info_6')
            result = cursor.fetchone()

            if result['@register_info_6'] == 1:
                resp = {"code": 1, "message": "重复注册"}
                return JsonResponse(resp)

    resp = {"code": 0,
            "message": "注册成功"}
    return JsonResponse(resp)


@csrf_exempt
def login_info(request):
    request_dict = json.loads(request.body.decode('utf-8'))

    # 准备存储过程的参数
    params = [
        request_dict["collegeId"],
        request_dict["password"],
        0, 0, '', '', 0
    ]

    connection = create_connection()
    # 调用存储过程并处理结果
    with connection:
        with connection.cursor() as cursor:
            cursor.callproc('login_info', params)
            cursor.execute("SELECT @_login_info_2, @_login_info_3, @_login_info_4, @_login_info_5, @_login_info_6")
            result = cursor.fetchone()
            user_id = result['@_login_info_2']
            user_type = result['@_login_info_3']
            user_name = result['@_login_info_4']
            stored_password = result['@_login_info_5']
            found = result['@_login_info_6']

            if found == 0:
                resp = {"code": 1, "message": "用户不存在"}
                return JsonResponse(resp)
            elif stored_password == request_dict["password"]:
                resp = {
                    "code": 0,
                    "message": "登陆成功",
                    "userId": str(user_id),
                    "userType": user_type,
                    "userName": user_name
                }
                return JsonResponse(resp)
            else:
                resp = {"code": 2, "message": "密码错误"}
                return JsonResponse(resp)


@csrf_exempt
def update_user_info(request):
    request_dict = json.loads(request.body.decode('utf-8'))

    # 获取要更新的用户信息
    user_id = request_dict.get("userId")
    new_email = request_dict.get("email")
    new_telephone = request_dict.get("telephone")
    new_intro = request_dict.get("userIntro")

    params = [
        user_id,
        new_email,
        new_telephone,
        new_intro
    ]

    # 创建数据库连接
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 调用存储过程
            cursor.callproc('update_user_info', params)
            connection.commit()

    return JsonResponse({"code": 0,
                         "message": "用户信息更新成功"})


@csrf_exempt
def change_password(request):
    request_dict = json.loads(request.body.decode('utf-8'))

    # 获取学号和新密码
    user_id = request_dict.get("userId")
    new_password = request_dict.get("newPassword")

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.callproc('change_password', [user_id, new_password])

    # 返回成功响应
    return JsonResponse({"code": 0, "message": "密码已成功更新"})


@csrf_exempt
def get_user_info(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")

    connection = create_connection()
    # 调用存储过程获取用户信息
    with connection:
        with connection.cursor() as cursor:
            cursor.callproc('get_user_info', [user_id, 0, '', '', '', '', 0])
            cursor.execute("SELECT @_get_user_info_1, @_get_user_info_2, @_get_user_info_3, @_get_user_info_4, "
                           "@_get_user_info_5, @_get_user_info_6")
            result = cursor.fetchone()
            college_id = result['@_get_user_info_1']
            user_name = result['@_get_user_info_2']
            email = result['@_get_user_info_3']
            telephone = result['@_get_user_info_4']
            user_intro = result['@_get_user_info_5']
            volunteer_time = result['@_get_user_info_6']

    # 返回用户信息
    return JsonResponse({
        "code": 0,
        "message": "获取信息成功",
        "telephone": telephone,
        "email": email,
        "volunteerTime": volunteer_time,
        "userIntro": user_intro
    })


@csrf_exempt
def user_get_message(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")

    message_list = []
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 调用存储过程
            cursor.callproc('user_get_message', [user_id])

            # 查询临时表获取消息
            cursor.execute('SELECT * FROM temp_messages')
            messages = cursor.fetchall()

            for message in messages:
                message_list.append({
                    'id': message['messageId'],
                    'time': message['messageTime'].strftime("%Y-%m-%d %H:%M"),
                    'title': message['messageTitle'],
                    'content': message['messageContent'],
                    'isRead': True if message['messageIsRead'] == 'True' else False
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

    # 创建数据库连接
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 调用存储过程
            cursor.callproc('user_read_message', [message_id])
            connection.commit()

    return JsonResponse({
        'code': 0,
        'message': '信息状态修改成功'
    })


@csrf_exempt
def upload_user_avatar(request):
    user_id = request.POST.get("userId")
    img = request.FILES["userAvatar"]

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

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'insert into image(imageName,imageURL) values (%s,%s)',
                [img_name, img_path]
            )

            cursor.execute('SELECT LAST_INSERT_ID()')
            image_id = cursor.fetchone()['LAST_INSERT_ID()']

            # 更新user的 avatarId 字段
            cursor.execute(
                'UPDATE user SET avatarId = %s WHERE userId = %s',
                [image_id, user_id]
            )
            connection.commit()

    # 返回头像
    try:
        with open(img_path, 'rb') as f:
            img = f.read()
            img = base64.b64encode(img)
            return HttpResponse(img, content_type='image/jpeg')
    except IOError:
        # 图片文件不存在或无法打开
        return HttpResponse('Image not found', status=404)


@csrf_exempt
def get_user_avatar(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")
    print(user_id)
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # user avatarId
            cursor.execute("SELECT avatarId FROM user WHERE userId = %s", [user_id])
            result = cursor.fetchone()

            # 没有上传头像
            if result['avatarId'] is None:
                image_path = 'images/userAvatar/defaultUserAvatar.png'
                with open(image_path, 'rb') as f:
                    img = f.read()
                    img = base64.b64encode(img)
                return HttpResponse(img, content_type='image/jpeg')

            avatar_id = result['avatarId']

            # 查询头像的详细信息
            cursor.execute("SELECT imageURL FROM image WHERE imageId = %s", [avatar_id])
            avatar_info = cursor.fetchone()

            # 检查是否得到了imageURL
            if not avatar_info or not avatar_info['imageURL']:
                return HttpResponse('')

            image_path = avatar_info['imageURL']

            try:
                with open(image_path, 'rb') as f:
                    img = f.read()
                    img = base64.b64encode(img)
                return HttpResponse(img, content_type='image/jpeg')
            except IOError:
                # 图片文件不存在或无法打开
                return HttpResponse('Image not found', status=404)
