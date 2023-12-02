from datetime import datetime, timedelta

import pymysql
from django.http import JsonResponse
import json
from pymysql.cursors import DictCursor
from settings import DATABASES as db_conf
from django.views.decorators.csrf import csrf_exempt


def create_connection():
    return pymysql.connect(host=db_conf["default"]["HOST"],
                           user=db_conf["default"]["USER"],
                           password=db_conf["default"]["PASSWORD"],
                           database=db_conf["default"]["NAME"],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


@csrf_exempt
def admin_create_recruitment(request):
    request_dict = json.loads(request.body.decode('utf-8'))

    project_id = request_dict.get("projectId")
    start_time = request_dict.get("startTime")  # 格式: "YYYY-MM-DD HH:mm"
    end_time = request_dict.get("endTime")  # 格式: "YYYY-MM-DD HH:mm"
    due_time = request_dict.get("deadline")  # 格式: "YYYY-MM-DD HH:mm"

    # 将字符串时间转换为 datetime 对象
    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
    launch_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
    due_time = datetime.strptime(due_time, "%Y-%m-%d %H:%M")

    # 其余招募信息
    location = request_dict.get("location")
    hours = request_dict.get("hours")
    recruitment_type = request_dict.get("type")
    max_number = request_dict.get("maxNumber")

    # 通知内容
    message_title = request_dict.get('message').get('title')
    message_content = request_dict.get('message').get('content')

    connection = create_connection()
    with connection.cursor() as cursor:
        # 插入新招募
        cursor.execute("""
            INSERT INTO recruitment (startTime,endTime,launchTime,dueTime, location, volunteerHour, recruitmentType, 
            maximumNumber, projectId)
            VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s)
        """, [start_time, end_time, launch_time, due_time, location, hours, recruitment_type, max_number, project_id])

        # 发送通知

        # 先获取收藏该项目的user_ids
        cursor.execute("SELECT userId FROM user_favorite_project WHERE projectId = %s", [project_id])
        results = cursor.fetchall()
        user_ids = []
        for result in results:
            user_ids.append(result.get('userId'))
        # 发送通知
        for user_id in user_ids:
            cur_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            # 发送通知
            cursor.execute('insert into message(messageTime,messageTitle,messageContent,messageIsRead,receiverId) '
                           'values (%s,%s,%s,%s,%s)', [cur_time, message_title, message_content, 'False', user_id])

        connection.commit()
    return JsonResponse({"code": 0, "message": "招募发布成功"})


@csrf_exempt
def user_get_recruitment_list(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get('userId')

    connection = create_connection()
    with connection.cursor() as cursor:
        # 获取当前所有的招募
        cursor.execute("SELECT * FROM recruitment")
        all_recruitments = cursor.fetchall()

        # 获取该用户所参加的团队
        cursor.execute("SELECT teamId FROM team_member WHERE userId = %s", [user_id])
        results = cursor.fetchall()
        user_teams = []
        for result in results:
            team_id = result.get('teamId')
            user_teams.append(team_id)

        recruitment_list = []

        # 获取用户所报名的所有招募
        cursor.execute("SELECT recruitmentId FROM recruitment_user WHERE userId = %s", [user_id])
        results = cursor.fetchall()
        my_recruitments = []

        for result in results:
            my_recruitments.append(result.get('recruitmentId'))

        for recruitment in all_recruitments:
            recruitment_id = recruitment.get('recruitmentId')
            start_time = recruitment.get('startTime').strftime("%Y-%m-%d %H:%M")
            end_time = recruitment.get('endTime').strftime("%Y-%m-%d %H:%M")
            launch_time = recruitment.get('launchTime').strftime("%Y-%m-%d %H:%M")
            dueTime = recruitment.get('dueTime').strftime("%Y-%m-%d %H:%M")
            location = recruitment.get('location')
            volunteer_hour = recruitment.get('volunteerHour')
            recruitment_type = recruitment.get('recruitmentType')
            maximum_number = recruitment.get('maximumNumber')
            project_id = recruitment.get('projectId')

            cursor.execute("SELECT teamId FROM recruitment_team WHERE recruitmentId = %s", [recruitment_id])
            recruitment_team_id = cursor.fetchone().get('teamId')

            if recruitment_team_id in user_teams or recruitment_type == "1":
                # 获取项目信息
                cursor.execute("SELECT projectName,projectType FROM project WHERE projectId = %s", [project_id])
                project = cursor.fetchone()
                project_name = project.get('projectName')
                project_type = project.get('projectType')

                # 获取当前招募人数
                cursor.execute("SELECT COUNT(*) FROM recruitment_user WHERE recruitmentId = %s", [recruitment_id])
                cur_number = cursor.fetchone().get('COUNT(*)')

                if recruitment_id in my_recruitments:
                    is_attend = True
                else:
                    is_attend = False

                recruitment_list.append({
                    'id': recruitment_id,
                    'launchTime': launch_time,
                    'dueTime': dueTime,
                    'startTime': start_time,
                    'endTime': end_time,
                    'location': location,
                    'volunteerHour': volunteer_hour,
                    'isAttend': is_attend,
                    'type': recruitment_type,
                    'maxNumber': maximum_number,
                    'currentNumber': cur_number,
                    'projectId': project_id,
                    'projectName': project_name,
                    'projectType': project_type,
                })

        connection.commit()
    recruitment_list = sorted(recruitment_list, key=lambda k: k['launchTime'])
    return JsonResponse({
        'code': 0,
        'message': '招募列表获取成功',
        'recruitmentList': recruitment_list
    })


@csrf_exempt
def user_get_my_recruitments(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get('userId')

    connection = create_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT recruitmentId FROM recruitment_user WHERE userId = %s", [user_id])
        results = cursor.fetchall()

        future_recruitment_list = []
        past_recruitment_list = []

        for result in results:
            recruitment_id = result.get('recruitmentId')
            cursor.execute("SELECT * FROM recruitment WHERE recruitmentId = %s", [recruitment_id])
            recruitment = cursor.fetchone()

            start_time = recruitment.get('startTime').strftime("%Y-%m-%d %H:%M")
            end_time = recruitment.get('endTime').strftime("%Y-%m-%d %H:%M")
            location = recruitment.get('location')
            volunteer_hour = recruitment.get('volunteerHour')
            recruitment_type = recruitment.get('recruitmentType')
            maximum_number = recruitment.get('maximumNumber')
            project_id = recruitment.get('projectId')

            # 获取项目信息
            cursor.execute("SELECT projectName,projectType FROM project WHERE projectId = %s", [project_id])
            project = cursor.fetchone()
            project_name = project.get('projectName')
            project_type = project.get('projectType')

            # 获取当前招募人数
            cursor.execute("SELECT COUNT(*) FROM recruitment_user WHERE recruitmentId = %s", [recruitment_id])
            participant_number = cursor.fetchone().get('COUNT(*)')

            cur_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")

            if cur_time < end_time:
                future_recruitment_list.append({
                    'id': recruitment_id,
                    'startTime': start_time,
                    'endTime': end_time,
                    'location': location,
                    'volunteerHour': volunteer_hour,
                    'type': recruitment_type,
                    'maxNumber': maximum_number,
                    'participantNumber': participant_number,
                    'projectId': project_id,
                    'projectName': project_name,
                    'projectType': project_type,
                })
            else:
                past_recruitment_list.append({
                    'id': recruitment_id,
                    'startTime': start_time,
                    'endTime': end_time,
                    'location': location,
                    'volunteerHour': volunteer_hour,
                    'type': recruitment_type,
                    'maxNumber': maximum_number,
                    'participantNumber': participant_number,
                    'projectId': project_id,
                    'projectName': project_name,
                    'projectType': project_type,
                })
        connection.commit()

    future_recruitment_list = sorted(future_recruitment_list, key=lambda k: k['startTime'])
    past_recruitment_list = sorted(past_recruitment_list, key=lambda k: k['startTime'])

    return JsonResponse({
        'code': 0,
        'futureRecruitmentList': future_recruitment_list,
        'pastRecruitmentList': past_recruitment_list
    })


@csrf_exempt
def user_apply_for_recruitment(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get('userId')
    recruitment_id = request_dict.get('recruitmentId')

    connection = create_connection()
    with connection.cursor() as cursor:
        # 报名招募
        cur_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
        cursor.execute("""
                    INSERT INTO recruitment_user (recruitmentId,userId,joinTime)
            VALUES (%s,%s,%s) """, [recruitment_id, user_id,cur_time])
        connection.commit()

    return JsonResponse({
        'code': 0,
        'message': '报名成功'
    })
