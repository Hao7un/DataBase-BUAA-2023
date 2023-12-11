import base64
import os

import pymysql
from django.http import HttpResponse
from django.http import JsonResponse
import json
from pymysql.cursors import DictCursor
from settings import DATABASES as db_conf
from settings import IMAGE_PATH
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta


def create_connection():
    return pymysql.connect(host=db_conf["default"]["HOST"],
                           user=db_conf["default"]["USER"],
                           password=db_conf["default"]["PASSWORD"],
                           database=db_conf["default"]["NAME"],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


"""
管理员相关的函数
- create_team               创建团队
- update_team_info          更新团队信息
- remove_team_member        删除团队成员
- review_team_application   审核团队申请
- get_all_managed_teams     获取所有管理的团队的信息
- get_managed_team_details          获取特定管理团队的详情信息
"""


@csrf_exempt
def admin_create_team(request):
    team_name = request.POST.get("teamName")
    team_intro = request.POST.get("teamIntro")
    team_leader_id = request.POST.get("userId")

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 调用存储过程
            cursor.callproc('admin_create_team', [team_name, team_intro, team_leader_id, 0, 0])
            cursor.execute('SELECT @_admin_create_team_3,@_admin_create_team_4')
            result = cursor.fetchone()
            code = result['@_admin_create_team_3']
            team_id = result['@_admin_create_team_4']

            if code == 1:
                return JsonResponse({
                    'code': 1,
                    'message': '存在同名的团队'
                })

            # 头像部分
            if 'teamAvatar' in request.FILES:
                img = request.FILES['teamAvatar']
                # 文件名
                img_name = img.name
                img_name = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S") + img_name

                # 存储的文件夹
                img_dir = IMAGE_PATH + 'teamAvatar/' + str(team_id)
                img_path = img_dir + '/' + img_name
                if not os.path.exists(img_dir):
                    os.makedirs(img_dir)

                with open(img_path, 'wb+') as destination:
                    for chunk in img.chunks():
                        destination.write(chunk)

                cursor.execute(
                    'insert into image(imageName,imageURL) values (%s,%s)',
                    [img_name, img_path]
                )

                cursor.execute('SELECT LAST_INSERT_ID()')
                image_id = cursor.fetchone()['LAST_INSERT_ID()']

                # 更新项目的 avatarId 字段
                cursor.execute(
                    'UPDATE team SET avatarId = %s WHERE teamId = %s',
                    [image_id, team_id]
                )

            connection.commit()

    return JsonResponse({
        "code": 0,
        "message": '创建团队成功'
    })


@csrf_exempt
def admin_get_all_teams(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('admin_get_all_teams', [user_id, ''])
        cursor.execute('SELECT @_admin_get_all_teams_1')
        result = cursor.fetchone()
        team_list_raw = result['@_admin_get_all_teams_1']

        # 解析团队信息
        team_list = []
        team_entries = team_list_raw.split(',')
        team_entries = team_entries[1:]
        for entry in team_entries:
            team_details = entry.split('|')
            team_list.append({
                "teamId": team_details[0],
                "name": team_details[1],
                "date": team_details[2],
                "number": int(team_details[3]),
                "hours": str(team_details[4]),
                "hasApplication": team_details[5] != '0'
            })
    return JsonResponse({
        "code": 0,
        "message": "获取成功",
        "teamList": team_list
    })


@csrf_exempt
def admin_update_team_info(request):
    request_dict = json.loads(request.body.decode('utf-8'))

    # 从请求中获取数据
    team_id = request_dict.get("teamId")
    new_team_name = request_dict.get("newTeamName")
    new_team_intro = request_dict.get("newTeamIntro")

    # 创建数据库连接
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 调用存储过程
            cursor.callproc('admin_update_team_info', [team_id, new_team_name, new_team_intro, 0])
            cursor.execute('SELECT @_admin_update_team_info_3')
            code = cursor.fetchone()['@_admin_update_team_info_3']
            connection.commit()

    if code == 0:
        message = '团队信息更新成功'
    else:
        message = '存在同名团队'

    return JsonResponse({"code": code,
                         "message": message})


@csrf_exempt
def admin_remove_team_member(request):  # 管理员删除团队成员
    request_dict = json.loads(request.body.decode('utf-8'))

    # 从请求中获取团队ID和用户ID
    team_id = request_dict.get("teamId")
    user_id = request_dict.get("userId")

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 删除团队成员
            cursor.callproc('admin_remove_team_member', [team_id, user_id])
            connection.commit()

    return JsonResponse({"code": 0, "message": "团队成员删除成功"})


@csrf_exempt
def admin_review_team_application(request):
    request_dict = json.loads(request.body.decode('utf-8'))

    # 从请求中获取参数
    team_id = request_dict.get("teamId")
    user_id = request_dict.get("userId")
    approved = request_dict.get("approved")
    approved = True if approved.lower() == 'true' else False

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('admin_review_team_application',
                        [team_id, user_id, approved])

    return JsonResponse({"code": 0,
                         "message": "审核完成"})


@csrf_exempt
def admin_get_specific_team_details(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    team_id = request_dict.get("teamId")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('admin_get_specific_team_details', [team_id, '', '', ''])
        cursor.execute('SELECT @_admin_get_specific_team_details_1,@_admin_get_specific_team_details_2,'
                       '@_admin_get_specific_team_details_3')
        result = cursor.fetchone()
        team_info_raw = result['@_admin_get_specific_team_details_1']
        application_list_raw = result['@_admin_get_specific_team_details_2']
        member_list_raw = result['@_admin_get_specific_team_details_3']

        # 解析团队信息
        details = team_info_raw.split('|')
        team_name = details[0]
        foundation_date = details[1]
        team_intro = details[2]
        total_hours = details[3]

        # 解析申请列表
        application_list = []
        application_entries = application_list_raw.split(',')
        application_entries = application_entries[1:]
        for entry in application_entries:
            details = entry.split('|')
            application_list.append({
                "userId": details[0],
                "date": details[1],
                "collegeId": details[2],
                "name": details[3]
            })

        # 解析团队成员列表
        member_list = []
        member_entries = member_list_raw.split(',')
        member_entries = member_entries[1:]
        for entry in member_entries:
            details = entry.split('|')
            member_list.append({
                "userId": details[0],
                "joinDate": details[1],
                "collegeId": details[2],
                "name": details[3],
                "telephone": details[4]
            })

    return JsonResponse({
        "code": 0,
        "message": "查询成功",
        "teamName": team_name,
        "establishmentDate": foundation_date,
        "teamIntro": team_intro,
        "totalHours": total_hours,
        "applicationList": application_list,
        "memberList": member_list,
    })


@csrf_exempt
def admin_get_team_projects(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    team_id = request_dict.get("teamId")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('admin_get_team_projects', [team_id, ''])
        cursor.execute('SELECT @_admin_get_team_projects_1')

        result = cursor.fetchone()
        project_list_raw = result['@_admin_get_team_projects_1']

        # 解析项目列表
        project_list = []
        project_entries = project_list_raw.split(',')
        project_entries = project_entries[1:]
        for entry in project_entries:
            details = entry.split('|')
            project_list.append({
                "id": details[0],
                "name": details[1],
                "category": details[2],
                "createdDate": details[3],
                "hasComments": bool(int(details[4]))
            })
    return JsonResponse({
        "code": 0,
        "message": "获取团队项目信息成功",
        "projects": project_list
    })


"""
志愿者用户相关的函数：
- apply_to_join_team    申请加入团队
- get_volunteer_teams   获取该志愿者加入的团队
- get_team_details      获取特定团队的信息
- get_all_team_list      
"""


@csrf_exempt
def user_apply_to_join_team(request):
    request_dict = json.loads(request.body.decode('utf-8'))

    # 从请求中获取团队ID和用户ID
    team_id = request_dict.get("teamId")
    user_id = request_dict.get("userId")

    # 获取当前时间作为申请时间
    apply_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d")

    # 调用存储过程处理申请
    connection = create_connection()
    with connection.cursor() as cursor:
        cursor.callproc('user_apply_to_join_team', [team_id, user_id, apply_time, 0])

        # 获取存储过程的输出参数
        cursor.execute("SELECT @_user_apply_to_join_team_3")
        result = cursor.fetchone()
        if result['@_user_apply_to_join_team_3'] == 1:
            return JsonResponse({
                "code": 1,
                "message": "您已经提交过加入申请"
            })

    return JsonResponse({"code": 0,
                         "message": "申请成功提交"})


@csrf_exempt
def user_get_all_teams_info(request):
    connection = create_connection()
    with (connection.cursor() as cursor):
        # 调用存储过程
        cursor.callproc('user_get_all_teams_info', [''])
        cursor.execute('SELECT @_user_get_all_teams_info_0')
        result = cursor.fetchone()
        teams_info_raw = result['@_user_get_all_teams_info_0']

        # 解析团队信息
        teams = []
        team_entries = teams_info_raw.split(',')
        team_entries = team_entries[1:]
        for entry in team_entries:
            team_details = entry.split('|')
            teams.append({
                'id': team_details[0],
                'name': team_details[1],
                'date': team_details[2],
                'number': int(team_details[3]),
                'hours': str(team_details[4])
            })

    # 构建响应数据
    resp = {
        "code": 0,
        "message": "团队信息获取成功",
        "totalList": teams
    }

    # 返回JSON响应
    return JsonResponse(resp)


@csrf_exempt
def user_get_all_my_teams(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('user_get_all_my_teams', [user_id, ''])
        cursor.execute('SELECT @_user_get_all_my_teams_1')
        result = cursor.fetchone()
        team_list_raw = result['@_user_get_all_my_teams_1']

        # 解析团队信息
        team_list = []
        team_entries = team_list_raw.split(',')
        team_entries = team_entries[1:]
        for entry in team_entries:
            team_details = entry.split('|')
            team_list.append({
                'id': team_details[0],
                'name': team_details[1],
                'number': str(team_details[2]),
                'hours': str(team_details[3])
            })

    # 构建响应数据
    resp = {
        "code": 0,
        "message": "团队信息获取成功",
        "teamList": team_list
    }
    # 返回JSON响应
    return JsonResponse(resp)


@csrf_exempt
def user_get_specific_team_details(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")
    team_id = request_dict.get("teamId")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('user_get_specific_team_details', [user_id, team_id, '', 0, None])
        cursor.execute('SELECT @_user_get_specific_team_details_2,@_user_get_specific_team_details_3,'
                       '@_user_get_specific_team_details_4')
        result = cursor.fetchone()
        team_details_raw = result['@_user_get_specific_team_details_2']
        is_member = result['@_user_get_specific_team_details_3']
        join_date = result['@_user_get_specific_team_details_4']

        # 解析团队详情
        print(team_details_raw)
        team_details = team_details_raw.split('|')
        team_name = team_details[0]
        team_number = team_details[6]
        team_intro = team_details[1]
        foundation_date = team_details[2]
        team_leader = team_details[3]
        telephone = team_details[4]
        email = team_details[5]

        # 解析项目
        project_list_raw = team_details[7]
        project_list = []
        project_entries = project_list_raw.split(',')
        project_entries = project_entries[1:]
        for entry in project_entries:
            project_details = entry.split('-')
            project_list.append({
                "id": project_details[0],
                "name": project_details[1],
                "type": project_details[2],
                "times": str(project_details[3])
            })

    return JsonResponse({
        "code": 0,
        "message": "查询成功",

        # 加入于*
        "isTeamMember": True if is_member else False,
        "joinDate": join_date,

        # 团队的信息
        "teamName": team_name,
        "teamNumber": str(team_number),
        "teamIntro": team_intro,
        "foundationDate": foundation_date,
        "teamLeader": team_leader,
        "telephone": telephone,
        "email": email,

        # 项目的信息
        "projectList": project_list
    })


@csrf_exempt
def upload_team_avatar(request):
    team_id = request.POST.get("teamId")
    img = request.FILES["teamAvatar"]

    # 文件名
    img_name = img.name.split('/')[-1]
    img_name = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S") + img_name

    # 存储的文件夹
    img_dir = IMAGE_PATH + 'teamAvatar/' + team_id
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

            # 更新项目的 avatarId 字段
            cursor.execute(
                'UPDATE team SET avatarId = %s WHERE teamId = %s',
                [image_id, team_id]
            )
            connection.commit()

    return HttpResponse(None)


@csrf_exempt
def get_team_avatar(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    team_id = request_dict.get("teamId")

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT avatarId FROM team WHERE teamId = %s", [team_id])
            result = cursor.fetchone()

            # 没有上传头像
            if result['avatarId'] is None:
                image_path = 'images/teamAvatar/defaultTeamAvatar.png'
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
