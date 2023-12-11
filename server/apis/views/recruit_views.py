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
    start_time = datetime.strptime(request_dict.get("startTime"), "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(request_dict.get("endTime"), "%Y-%m-%d %H:%M")
    launch_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
    due_time = datetime.strptime(request_dict.get("deadline"), "%Y-%m-%d %H:%M")
    location = request_dict.get("location")
    hours = request_dict.get("hours")
    recruitment_type = request_dict.get("type")
    max_number = request_dict.get("maxNumber")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('admin_create_recruitment',
                        [project_id, start_time, end_time, launch_time, due_time, location,
                         hours, recruitment_type, max_number])
        connection.commit()

    return JsonResponse({"code": 0, "message": "招募发布成功"})


@csrf_exempt
def admin_get_recruitment_applicants(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    recruitment_id = request_dict.get('recruitmentId')

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('admin_get_recruitment_applicants', [recruitment_id, ''])
        cursor.execute('SELECT @_admin_get_recruitment_applicants_1')
        result = cursor.fetchone()
        applicant_list_raw = result['@_admin_get_recruitment_applicants_1']

        # 解析申请者信息
        recruits = []
        applicant_entries = applicant_list_raw.split(',')
        applicant_entries = applicant_entries[1:]
        for entry in applicant_entries:
            details = entry.split('|')
            recruits.append({
                "collegeId": details[0],
                "name": details[1],
                "telephone": details[2],
                "email": details[3],
                "time": details[4]
            })
    return JsonResponse({
        'code': 0,
        'message': '获取成功',
        'recruits': recruits
    })


@csrf_exempt
def user_get_recruitment_list(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get('userId')

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程，并传入用户ID
        cursor.callproc('user_get_recruitment_list', [user_id, ''])
        cursor.execute('SELECT @_user_get_recruitment_list_1')
        result = cursor.fetchone()
        recruitment_list_raw = result['@_user_get_recruitment_list_1']

        recruitment_list = []
        recruitment_entries = recruitment_list_raw.split(',')
        recruitment_entries = recruitment_entries[1:]
        for entry in recruitment_entries:
            recruitment_details = entry.split('|')
            recruitment_list.append({
                'id': recruitment_details[0],
                'launchTime': recruitment_details[1],
                'dueTime': recruitment_details[2],
                'startTime': recruitment_details[3],
                'endTime': recruitment_details[4],
                'location': recruitment_details[5],
                'volunteerHour': recruitment_details[6],
                'isAttend': recruitment_details[7] == '1',
                'type': recruitment_details[8],
                'maxNumber': recruitment_details[9],
                'currentNumber': recruitment_details[10],
                'projectId': recruitment_details[11],
                'projectName': recruitment_details[12],
                'projectType': recruitment_details[13],
            })

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
        # 调用存储过程，并传入用户ID
        cursor.callproc('user_get_my_recruitments', [user_id, '', ''])
        cursor.execute('SELECT @_user_get_my_recruitments_1,@_user_get_my_recruitments_2')
        result = cursor.fetchone()
        future_recruitments_raw = result['@_user_get_my_recruitments_1']
        past_recruitments_raw = result['@_user_get_my_recruitments_2']
        # 处理存储过程返回的数据
        future_recruitment_list = []
        recruitment_entries = future_recruitments_raw.split(',')
        recruitment_entries = recruitment_entries[1:]
        for entry in recruitment_entries:
            recruitment_details = entry.split('|')
            future_recruitment_list.append({
                'id': recruitment_details[0],
                'startTime': recruitment_details[1],
                'endTime': recruitment_details[2],
                'location': recruitment_details[3],
                'volunteerHour': recruitment_details[4],
                'type': recruitment_details[5],
                'maxNumber': recruitment_details[6],
                'projectId': recruitment_details[7],
                'projectName': recruitment_details[8],
                'projectType': recruitment_details[9],
                'participantNumber': recruitment_details[10],
            })

        past_recruitment_list = []
        recruitment_entries = past_recruitments_raw.split(',')
        recruitment_entries = recruitment_entries[1:]
        for entry in recruitment_entries:
            recruitment_details = entry.split('|')
            past_recruitment_list.append({
                'id': recruitment_details[0],
                'startTime': recruitment_details[1],
                'endTime': recruitment_details[2],
                'location': recruitment_details[3],
                'volunteerHour': recruitment_details[4],
                'type': recruitment_details[5],
                'maxNumber': recruitment_details[6],
                'projectId': recruitment_details[7],
                'projectName': recruitment_details[8],
                'projectType': recruitment_details[9],
                'participantNumber': recruitment_details[10],
            })

    return JsonResponse({
        'code': 0,
        'futureRecruitmentList': future_recruitment_list,
        'pastRecruitmentList': past_recruitment_list
    })


@csrf_exempt
def user_get_volunteer_statistics(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get('userId')

    # 设置学期的开始和结束日期
    current_year = datetime.now().year
    spring_semester_start = datetime(current_year, 2, 25)
    spring_semester_end = datetime(current_year, 6, 30)
    fall_semester_start = datetime(current_year, 9, 1)
    fall_semester_end = datetime(current_year + 1, 1, 15)

    connection = create_connection()
    with connection.cursor() as cursor:
        # 获取过去的招募信息
        cursor.callproc('user_get_my_recruitments', [user_id, '', ''])
        cursor.execute('SELECT @_user_get_my_recruitments_1,'
                       '@_user_get_my_recruitments_2')
        result = cursor.fetchone()
        past_recruitments_raw = result['@_user_get_my_recruitments_2']

        # 初始化统计数据
        total_hours = 0
        semester_hours = 0
        type_hours = {'type1': 0, 'type2': 0, 'type3': 0,
                      'type4': 0, 'type5': 0, 'type6': 0}
        monthly_hours = {month: 0 for month in ['january', 'february', 'march', 'april', 'may', 'june', 'july',
                                                'august', 'september', 'october', 'november', 'december']}

        # 处理数据
        recruitment_entries = past_recruitments_raw.split(',')[1:]
        for entry in recruitment_entries:
            details = entry.split('|')
            volunteer_hours = int(details[4])
            project_type = details[9]
            start_time = datetime.strptime(details[1], '%Y-%m-%d')

            total_hours += volunteer_hours
            # 判断是否属于当前学期
            if spring_semester_start <= start_time <= spring_semester_end or fall_semester_start <= start_time <= fall_semester_end:
                semester_hours += volunteer_hours

            type_hours[f'type{project_type}'] += volunteer_hours
            monthly_hours[start_time.strftime('%B').lower()] += volunteer_hours

        # 返回统计结果
        statistics = {
            'code': 0,
            'message': '',
            'total': total_hours,
            'semester': semester_hours,
            **type_hours,
            **monthly_hours
        }

        return JsonResponse(statistics)


@csrf_exempt
def user_apply_for_recruitment(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get('userId')
    recruitment_id = request_dict.get('recruitmentId')

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('user_apply_for_recruitment', [recruitment_id, user_id, 0])
        cursor.execute('SELECT @_user_apply_for_recruitment_2')
        result = cursor.fetchone()
        if result['@_user_apply_for_recruitment_2'] == 1:
            return JsonResponse({
                'code': 1,
                'message': '已经到达人数上限'
            })
        elif result['@_user_apply_for_recruitment_2'] == 2:
            return JsonResponse({
                'code': 2,
                'message': '与您参与的招募存在时间冲突'
            })

    return JsonResponse({
        'code': 0,
        'message': '报名成功'
    })
