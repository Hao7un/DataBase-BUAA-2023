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
def admin_create_team(request):  # 创建志愿团队
    request_dict = json.loads(request.body.decode('utf-8'))

    # 获取团队注册信息
    team_name = request_dict.get("teamName")
    team_intro = request_dict.get("teamIntro")
    team_leader_id = request_dict.get("userId")
    foundation_date = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d")

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 检查是否有团队同名
            cursor.execute("select * from team where teamName = %s", [team_name])
            result = cursor.fetchall()
            connection.commit()
            if len(result) != 0:
                resp = {
                    "code": 1,
                    "message": "团队名已存在"
                }
            # 插入数据库
            cursor.execute('insert into team(teamName,teamIntro,teamLeaderId,foundationDate) values(%s,%s,%s,%s)',
                           [team_name, team_intro, team_leader_id, foundation_date])

            # 获取团队id
            cursor.execute('SELECT teamId FROM team WHERE teamName = %s', [team_name])
            team_id = cursor.fetchall()[0]["teamId"]

            # 把自己插入团队中
            current_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO team_user(teamId, userId, date, status) VALUES (%s, %s, %s, %s)",
                           [team_id, team_leader_id, current_time, 'accepted'])

            connection.commit()

    return JsonResponse({"code": 0,
                         "message": "团队创建成功"})


@csrf_exempt
def admin_get_all_teams(request):  # 获取管理员管理的所有团队列表
    request_dict = json.loads(request.body.decode('utf-8'))
    userId = request_dict.get("userId")

    connection = create_connection()
    team_list = []

    with connection:
        with connection.cursor() as cursor:
            # 获取管理员管理的所有团队
            cursor.execute("SELECT teamId, teamName, foundationDate FROM team WHERE teamLeaderId = %s", [userId])
            teams = cursor.fetchall()

            for team in teams:
                team_id = team['teamId']
                team_name = team['teamName']
                foundation_date = team['foundationDate']

                # print(team_id)
                # 获取团队成员数量，从视图team_member之中获取
                cursor.execute("SELECT COUNT(*) FROM team_member WHERE teamId = %s", [team_id])

                number = cursor.fetchone()['COUNT(*)']

                # 获取团队所有成员的总志愿时长
                cursor.execute("SELECT totalTeamHours FROM team_volunteerHours WHERE teamId = %s", [team_id])
                result = cursor.fetchone()
                if result is None:
                    total_team_hours = 0
                else:
                    total_team_hours = result['totalTeamHours']

                # 检查是否有未处理的申请
                cursor.execute("SELECT COUNT(*) FROM team_user_pending WHERE teamId = %s", [team_id])
                has_application = cursor.fetchone()["COUNT(*)"] > 0

                # 添加到团队列表
                team_list.append({
                    "teamId": team_id,
                    "name": team_name,
                    "number": number,
                    "date": foundation_date,
                    "hours": str(total_team_hours),
                    "hasApplication": has_application
                })

    return JsonResponse({"code": 0, "message": "获取成功", "teamList": team_list})


@csrf_exempt
def admin_update_team_info(request):
    request_dict = json.loads(request.body.decode('utf-8'))

    # 从请求中获取数据
    team_id = request_dict.get("teamId")
    new_team_name = request_dict.get("newTeamName")
    new_team_intro = request_dict.get("newTeamIntro")

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 更新团队信息
            update_query = "UPDATE team SET "
            update_params = []
            if new_team_name:
                update_query += "teamName = %s, "
                update_params.append(new_team_name)
            if new_team_intro:
                update_query += "teamIntro = %s, "
                update_params.append(new_team_intro)
            update_query = update_query.rstrip(', ')
            update_query += " WHERE teamId = %s"
            update_params.append(team_id)

            cursor.execute(update_query, update_params)
            connection.commit()

    return JsonResponse({"code": 0, "message": "团队信息更新成功"})


@csrf_exempt
def admin_remove_team_member(request):  # 管理员删除团队成员
    request_dict = json.loads(request.body.decode('utf-8'))

    # 从请求中获取团队ID和用户ID
    team_id = request_dict.get("teamId")
    user_id = request_dict.get("userId")

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 检查指定的团队成员是否存在
            cursor.execute("SELECT * FROM team_member WHERE teamId = %s AND userId = %s", [team_id, user_id])
            if cursor.rowcount == 0:
                return JsonResponse({"code": 1, "message": "团队成员不存在"})

            # 删除团队成员
            cursor.execute("DELETE FROM team_member WHERE teamId = %s AND userId = %s", [team_id, user_id])
            connection.commit()

    return JsonResponse({"code": 0, "message": "团队成员删除成功"})


@csrf_exempt
def admin_review_team_application(request):
    request_dict = json.loads(request.body.decode('utf-8'))

    # 从请求中获取团队ID、用户ID和审核结果
    team_id = request_dict.get("teamId")
    user_id = request_dict.get("userId")

    # 要发送的message
    message_title = request_dict.get('message').get('title')
    message_content = request_dict.get('message').get('content')

    approved = request_dict.get("approved")
    approved = True if approved.lower() == 'true' else False

    print(team_id)
    print(user_id)
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 检查指定的申请是否存在
            cursor.execute("SELECT * FROM team_user_pending WHERE teamId = %s AND userId = %s", [team_id, user_id])
            if cursor.rowcount == 0:
                return JsonResponse({"code": 1, "message": "申请不存在"})

            # 更新申请状态
            new_status = 'accepted' if approved else 'rejected'
            cur_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("UPDATE team_user SET status = %s,date = %s WHERE teamId = %s AND userId = %s",
                           [new_status, cur_time, team_id, user_id])

            # 发送通知
            cursor.execute('insert into message(messageTime,messageTitle,messageContent,messageIsRead,receiverId) '
                           'values (%s,%s,%s,%s,%s)', [cur_time, message_title, message_content, 'False', user_id])

            connection.commit()

    return JsonResponse({"code": 0, "message": "审核完成"})


@csrf_exempt
def admin_get_specific_team_details(request):  # 获取某个管理团队详情
    request_dict = json.loads(request.body.decode('utf-8'))
    team_id = request_dict.get("teamId")
    # print(team_id)
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 查询团队介绍
            cursor.execute("SELECT teamIntro FROM team WHERE teamId = %s", [team_id])
            team_intro = cursor.fetchone()["teamIntro"] if cursor.rowcount > 0 else ""

            # 查询申请加入该团队的列表
            cursor.execute("""
                SELECT a.userId, a.date, u.collegeId, u.userName 
                FROM team_user_pending a
                JOIN user u ON a.userId = u.userId
                WHERE a.teamId = %s
            """, [team_id])

            applications = cursor.fetchall()
            application_list = [{
                "userId": str(app["userId"]),
                "collegeId": app["collegeId"],
                "name": app["userName"],
                "date": app["date"]
            } for app in applications]

            # 查询该团队的所有成员
            cursor.execute("""
                SELECT m.userId, m.date, u.collegeId, u.userName, u.telephone
                FROM team_member m
                JOIN user u ON m.userId = u.userId
                WHERE m.teamId = %s
            """, [team_id])
            members = cursor.fetchall()
            member_list = [{
                "userId": str(member["userId"]),
                "collegeId": member["collegeId"],
                "name": member["userName"],
                "telephone": member["telephone"],
                "joinDate": member["date"]
            } for member in members]

            # 查询该团队下的所有项目
            cursor.execute("""
                SELECT p.projectId, p.projectName, p.projectType, p.foundationDate,
                       EXISTS(
                           SELECT 1 
                           FROM question q 
                           WHERE q.projectId = p.projectId 
                           AND NOT EXISTS (
                               SELECT 1 
                               FROM reply r 
                               WHERE r.replyToId = q.questionId
                           )
                       ) as hasUnansweredQuestions
                FROM project p
                WHERE p.teamId = %s
            """, [team_id])

            projects = cursor.fetchall()

            project_list = [{
                "id": str(project["projectId"]),
                "name": project["projectName"],
                "category": project["projectType"],
                "createdDate": project["foundationDate"].strftime("%Y-%m-%d"),
                "hasComments": bool(project["hasUnansweredQuestions"])
            } for project in projects]

    return JsonResponse({
        "code": 0,
        "message": "查询成功",
        "teamIntro": team_intro,
        "applicationList": application_list,
        "memberList": member_list,
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
def user_apply_to_join_team(request):  # 申请加入团队
    request_dict = json.loads(request.body.decode('utf-8'))

    # 从请求中获取团队ID和用户ID
    team_id = request_dict.get("teamId")
    user_id = request_dict.get("userId")

    # 获取当前时间作为申请时间
    apply_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d")

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 检查用户是否已经申请加入该团队
            cursor.execute("SELECT * FROM team_user_pending WHERE teamId = %s AND userId = %s", [team_id, user_id])
            if cursor.rowcount != 0:
                return JsonResponse({"code": 1, "message": "您已经提交过申请"})

            # 插入申请信息
            cursor.execute("INSERT INTO team_user_pending (teamId, userId, date, status) VALUES (%s, %s, %s, %s)",
                           [team_id, user_id, apply_time, 'pending'])
            connection.commit()

    return JsonResponse({"code": 0, "message": "申请成功提交"})


@csrf_exempt
def user_get_all_teams_info(request):
    connection = create_connection()
    with connection.cursor() as cursor:
        # 执行SQL查询以获取所有团队信息
        cursor.execute('SELECT teamId, teamName,foundationDate FROM team')
        # 获取查询结果
        teams_data = cursor.fetchall()

    # 处理查询结果
    teams = []
    for team_data in teams_data:
        team_id = team_data.get("teamId")
        team_name = team_data.get("teamName")
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM team_member WHERE teamId = %s", [team_id])
            team_number = cursor.fetchone()["COUNT(*)"]
            cursor.execute("SELECT totalTeamHours FROM team_volunteerHours WHERE teamId = %s", [team_id])
            result = cursor.fetchone()
            if result == None:
                total_team_hours = 0
            else:
                total_team_hours = result["totalTeamHours"]

        foundation_date = team_data.get("foundationDate")
        teams.append({
            'id': team_id,
            'name': team_name,
            'number': int(team_number),
            'date': foundation_date.strftime('%Y-%m-%d'),
            'hours': str(total_team_hours)
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
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT teamId FROM team_member WHERE userId = %s",
                           [user_id])
            teams = cursor.fetchall()

            team_list = []
            for team in teams:
                team_id = team.get("teamId")
                cursor.execute("SELECT teamName FROM team WHERE teamId = %s", [team_id])
                team_name = cursor.fetchone()["teamName"]
                cursor.execute("SELECT COUNT(*) FROM team_member WHERE teamId = %s", [team_id])
                team_number = cursor.fetchone()["COUNT(*)"]
                cursor.execute("SELECT totalTeamHours FROM team_volunteerHours WHERE teamId = %s", [team_id])
                result = cursor.fetchone()
                if result == None:
                    total_team_hours = 0
                else:
                    total_team_hours = result["totalTeamHours"]
                team_list.append({
                    "id": team_id,
                    "name": team_name,
                    "number": str(team_number),
                    "hours": str(total_team_hours)  # 假设 total_hours 已计算
                })
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
    with connection:
        with connection.cursor() as cursor:
            # 检查是否为团队成员
            cursor.execute("SELECT COUNT(*),date FROM team_member WHERE teamId = %s And userId = %s",
                           [team_id, user_id])
            result = cursor.fetchone()
            is_member = True if result["COUNT(*)"] == 1 else False
            if is_member:
                join_date = result.get('date')
            else:
                join_date = "N/A"

            # 获取团队信息
            cursor.execute("SELECT teamName, teamIntro, foundationDate, teamLeaderId FROM team WHERE teamId = %s",
                           [team_id])
            team_info = cursor.fetchone()
            if not team_info:
                return JsonResponse({"code": 1, "message": "团队不存在"})

            team_name = team_info.get("teamName")
            team_intro = team_info.get("teamIntro")
            foundation_date = team_info.get("foundationDate")
            team_leader_id = team_info.get("teamLeaderId")

            # 获取团队领导者的信息
            cursor.execute("SELECT userName, telephone, email FROM user WHERE userId = %s", [team_leader_id])
            leader_info = cursor.fetchone()

            team_leader = leader_info.get("userName")
            telephone = leader_info.get("telephone")
            email = leader_info.get("email")

            # 获取团队成员数量
            cursor.execute("SELECT COUNT(*) FROM team_member WHERE teamId = %s", [team_id])
            team_number = cursor.fetchone()["COUNT(*)"]

            # 获取团队参与的项目列表
            cursor.execute("SELECT projectId, projectName, projectType FROM project WHERE teamId = %s", [team_id])
            projects = cursor.fetchall()

            project_list = []
            for project in projects:
                project_id = project["projectId"]
                project_name = project["projectName"]
                project_type = project["projectType"]
                cursor.execute("SELECT recruitCount FROM project_recruit_count WHERE projectId = %s", [project_id])
                result = cursor.fetchone()
                if result is None:
                    recruit_count = '0'
                else:
                    recruit_count = result['recruitCount']

                project_list.append({
                    "id": project_id,
                    "name": project_name,
                    "type": project_type,
                    "times": recruit_count
                })

    return JsonResponse({
        "code": 0,
        "message": "查询成功",
        "isTeamMember": True if is_member else False,
        "teamName": team_name,
        "teamNumber": str(team_number),
        "teamIntro": team_intro,
        "foundationDate": foundation_date,
        "joinDate": join_date,
        "teamLeader": team_leader,
        "telephone": telephone,
        "email": email,
        "projectList": project_list
    })


@csrf_exempt
def upload_team_avatar(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    team_id = request_dict.get("teamId")
    img = request.FILES["file"]

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
            # 查询team的 avatarId
            cursor.execute("SELECT avatarId FROM team WHERE teamId = %s", [team_id])
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
