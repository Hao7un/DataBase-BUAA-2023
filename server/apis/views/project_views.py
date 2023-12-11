import base64
import os
from datetime import datetime, timedelta

import pymysql
from django.http import JsonResponse, HttpResponse
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


"""
管理员管理部分
"""


@csrf_exempt
def admin_create_project(request):
    project_name = request.POST.get("projectName")
    project_type = request.POST.get("projectType")
    project_intro = request.POST.get("projectIntro")
    team_id = request.POST.get("teamId")
    foundation_date = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('admin_create_project',
                        [project_name, project_type, project_intro, foundation_date, team_id, 0, 0])
        cursor.execute('SELECT @_admin_create_project_5,@_admin_create_project_6')
        result = cursor.fetchone()
        project_id = result['@_admin_create_project_5']
        code = result['@_admin_create_project_6']

        if code == 1:
            return JsonResponse({"code": 1,
                                 "message": "已存在同名项目"})

        # 头像部分
        if 'projectAvatar' in request.FILES:
            img = request.FILES["projectAvatar"]

            # 文件名
            img_name = img.name
            img_name = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S") + img_name

            # 存储的文件夹
            img_dir = IMAGE_PATH + 'projectAvatar/' + str(project_id)
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
                'UPDATE project SET avatarId = %s WHERE projectId = %s',
                [image_id, project_id]
            )
        connection.commit()

    return JsonResponse({"code": 0,
                         "message": "项目创建成功"})


@csrf_exempt
def admin_update_project_info(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    project_id = request_dict.get("projectId")
    new_project_name = request_dict.get("newProjectName")
    new_project_intro = request_dict.get("newProjectIntro")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 更新项目信息
        cursor.callproc('admin_update_project_info',
                        [project_id, new_project_name, new_project_intro, 0])

        # 获取是否更新成功
        cursor.execute('SELECT @_admin_update_project_info_3')
        code = cursor.fetchone()['@_admin_update_project_info_3']
        connection.commit()

    if code == 0:
        message = "项目信息更新成功"
    else:
        message = "存在同名项目"
    return JsonResponse({"code": code,
                         "message": message})


@csrf_exempt
def admin_create_tutorial(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    project_id = request_dict.get("projectId")
    tutorial_title = request_dict.get("tutorialTitle")
    tutorial_tag = request_dict.get("tutorialTag")
    tutorial_content = request_dict.get("tutorialContent")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 创建新教程
        current_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.callproc('admin_create_tutorial', [project_id, current_time,
                                                  tutorial_title, tutorial_tag, tutorial_content])
        connection.commit()

    return JsonResponse({"code": 0,
                         "message": "教程创建成功"})


@csrf_exempt
def admin_update_tutorial(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    tutorial_id = request_dict.get("tutorialId")
    new_tutorial_title = request_dict.get("newTutorialTitle")
    new_tutorial_tag = request_dict.get("newTutorialTag")
    new_tutorial_content = request_dict.get("newTutorialContent")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 更新教程信息
        cursor.callproc('admin_update_tutorial', [tutorial_id, new_tutorial_title,
                                                  new_tutorial_tag, new_tutorial_content])
        connection.commit()

    return JsonResponse({"code": 0,
                         "message": "教程信息更新成功"})


@csrf_exempt
def admin_delete_tutorial(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    tutorial_id = request_dict.get("tutorialId")
    connection = create_connection()

    with connection.cursor() as cursor:
        # 删除教程
        cursor.callproc("admin_delete_tutorial", [tutorial_id])
        connection.commit()

    return JsonResponse({"code": 0,
                         "message": "教程删除成功"})


@csrf_exempt
def admin_reply_question(request):
    request_dict = json.loads(request.body.decode('utf-8'))

    # 获取请求中的参数
    question_id = request_dict.get("questionId")
    user_id = request_dict.get("userId")
    reply_content = request_dict.get("replyContent")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('admin_reply_question', [question_id, user_id, reply_content])

    return JsonResponse({"code": 0,
                         "message": "回复成功"})


@csrf_exempt
def admin_get_project_details(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    project_id = request_dict.get("projectId")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('admin_get_project_details', [project_id, '', '', ''])
        cursor.execute(
            'SELECT @_admin_get_project_details_1,@_admin_get_project_details_2,@_admin_get_project_details_3')
        result = cursor.fetchone()
        project_info_raw = result['@_admin_get_project_details_1']
        unreplied_questions_raw = result['@_admin_get_project_details_2']
        tutorials_raw = result['@_admin_get_project_details_3']

        # 解析项目信息
        details = project_info_raw.split('|')
        project_name = details[0]
        project_type = details[1]
        project_intro = details[2]
        foundation_date = details[3]

        # 解析未回复提问列表
        unreplied_questions = []
        unreplied_questions_entries = unreplied_questions_raw.split(',')
        unreplied_questions_entries = unreplied_questions_entries[1:]
        for entry in unreplied_questions_entries:
            details = entry.split('|')
            unreplied_questions.append({
                "questionId": details[0],
                "date": details[1],
                "posterId": details[2],
                "content": details[3],
                "posterName": details[4]
            })

        # 解析教程列表
        tutorials = []
        tutorial_entries = tutorials_raw.split(',')
        tutorial_entries = tutorial_entries[1:]
        for entry in tutorial_entries:
            details = entry.split('|')
            tutorials.append({
                "id": details[0],
                "title": details[1],
                "content": details[2],
                "date": details[3],
                "tag": details[4]
            })

    return JsonResponse({
        "code": 0,
        "message": "获取项目信息成功",
        "projectName": project_name,
        "projectType": project_type,
        "projectIntro": project_intro,
        "createdDate": foundation_date,
        "comments": unreplied_questions,
        "tutorials": tutorials
    })


@csrf_exempt
def admin_get_project_recruitments(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    project_id = request_dict.get("projectId")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('admin_get_project_recruitments', [project_id, ''])
        cursor.execute('SELECT @_admin_get_project_recruitments_1')
        result = cursor.fetchone()
        recruitment_list_raw = result['@_admin_get_project_recruitments_1']

        # 解析招募信息
        recruitments = []
        recruitment_entries = recruitment_list_raw.split(',')
        recruitment_entries = recruitment_entries[1:]
        for entry in recruitment_entries:
            details = entry.split('|')
            recruitments.append({
                "id": details[0],
                "launchTime": details[3],
                "deadline": details[4],
                "startTime": details[1],
                "endTime": details[2],
                "location": details[5],
                "type": details[6],
                "hours": details[7],
                "number": details[9],
                "maxNumber": details[8]
            })
    return JsonResponse({
        'code': 0,
        'recruitments': recruitments
    })


"""
用户管理部分
"""


@csrf_exempt
def user_post_question(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")
    project_id = request_dict.get("projectId")
    post_content = request_dict.get("question")
    connection = create_connection()
    with connection.cursor() as cursor:
        # 插入提问数据到question表
        cursor.callproc('user_post_question', [(datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"),
                                               post_content, project_id, user_id])
        connection.commit()

    return JsonResponse({"code": 0,
                         "message": "提问成功"})


@csrf_exempt
def user_get_all_projects(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")


    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('user_get_all_projects', [user_id, ''])
        cursor.execute('SELECT @_user_get_all_projects_1')
        result = cursor.fetchone()
        project_list_raw = result['@_user_get_all_projects_1']

        # 解析项目列表
        project_list = []
        project_entries = project_list_raw.split(',')
        project_entries = project_entries[1:]
        for entry in project_entries:
            project_details = entry.split('|')
            project_list.append({
                "id": project_details[0],
                "name": project_details[1],
                "type": project_details[2],
                "team": project_details[3],
                "isMyTeam": project_details[4] == '1',
                "latestTime": project_details[5]
            })
    resp = {
        "code": 0,
        "message": "项目信息获取成功",
        "projectList": project_list
    }

    return JsonResponse(resp)


@csrf_exempt
def user_get_specific_project(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")
    project_id = request_dict.get("projectId")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('user_get_specific_project', [user_id, project_id, 0, '', '', ''])
        cursor.execute('SELECT @_user_get_specific_project_2,@_user_get_specific_project_3,'
                       '@_user_get_specific_project_4,@_user_get_specific_project_5')
        result = cursor.fetchone()
        is_collected = result['@_user_get_specific_project_2']
        is_collected = True if is_collected == 1 else False
        project_details_raw = result['@_user_get_specific_project_3']
        discussions_raw = result['@_user_get_specific_project_4']
        tutorials_raw = result['@_user_get_specific_project_5']

        # 解析项目详情
        project_details = project_details_raw.split('|')

        # 解析讨论区信息
        discussion_list = []
        discussions = discussions_raw.split(',')
        discussions = discussions[1:]
        for disc in discussions:
            details = disc.split('|')
            discussion_list.append({
                "questionPoster": details[0],
                "questionTime": details[1],
                "question": details[2],
                "replyTime": details[3],
                "reply": details[4]
            })

        # 解析教程信息
        tutorial_list = []
        tutorials = tutorials_raw.split(',')
        tutorials = tutorials[1:]
        for tut in tutorials:
            details = tut.split('|')
            tutorial_list.append({
                "id": details[0],
                "time": details[1],
                "title": details[2],
                "tag": details[3],
                "content": details[4]
            })

    return JsonResponse({
        "code": 0,
        "message": "获取特定团队的信息成功",
        "isCollect": is_collected,
        "projectName": project_details[0],
        "projectType": project_details[1],
        "projectIntro": project_details[2],
        "teamId": str(project_details[3]),
        "teamName": project_details[4],
        "latestTime": project_details[5],
        "projectLeader": project_details[6],
        "discussionList": discussion_list,
        "tutorialList": tutorial_list
    })


@csrf_exempt
def user_get_favorite_projects(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('user_get_favorite_projects', [user_id, ''])
        cursor.execute('SELECT @_user_get_favorite_projects_1')
        result = cursor.fetchone()
        project_list_raw = result['@_user_get_favorite_projects_1']

        # 解析项目列表
        project_list = []
        project_entries = project_list_raw.split(',')
        project_entries = project_entries[1:]

        for entry in project_entries:
            project_details = entry.split('|')
            project_list.append({
                "id": project_details[0],
                "name": project_details[1],
                "type": project_details[2],
                "team": project_details[3],
                "latestTime": project_details[4]
            })
    resp = {
        "code": 0,
        "message": "收藏项目信息获取成功",
        "projectList": project_list
    }
    return JsonResponse(resp)


@csrf_exempt
def user_toggle_favorite_project(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")
    project_id = request_dict.get("projectId")
    connection = create_connection()

    with connection.cursor() as cursor:
        cursor.callproc('user_toggle_favorite_project', [user_id, project_id])
        connection.commit()

    resp = {
        "code": 0,
        "message": '修改成功'
    }

    return JsonResponse(resp)


@csrf_exempt
def upload_project_avatar(request):
    project_id = request.POST.get("projectId")
    img = request.FILES["projectAvatar"]

    # 文件名
    img_name = img.name.split('/')[-1]
    img_name = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S") + img_name

    # 存储的文件夹
    img_dir = IMAGE_PATH + 'projectAvatar/' + project_id
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
                'UPDATE project SET avatarId = %s WHERE projectId = %s',
                [image_id, project_id]
            )
            connection.commit()

    return HttpResponse(None)


@csrf_exempt
def get_project_avatar(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    project_id = request_dict.get("projectId")
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 查询project的 avatarId
            cursor.execute("SELECT avatarId FROM project WHERE projectId = %s", [project_id])
            result = cursor.fetchone()

            # 没有上传头像
            if result['avatarId'] is None:
                image_path = 'images/projectAvatar/defaultProjectAvatar.png'
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
                return HttpResponse('Image not found',
                                    status=404)
