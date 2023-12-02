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
    #request_dict = json.loads(request.body.decode('utf-8'))
    #project_name = request_dict.get("projectName")
    #project_type = request_dict.get("projectType")
    #project_intro = request_dict.get("projectIntro")
    #team_id = request_dict.get("teamId")

    project_name = request.POST.get("projectName")
    project_type = request.POST.get("projectType")
    project_intro = request.POST.get("projectIntro")
    team_id = request.POST.get("teamId")

    foundation_date = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 检查是否存在重名的项目
        cursor.execute("SELECT COUNT(*) FROM project WHERE projectName = %s", [project_name])
        if cursor.fetchone()['COUNT(*)'] > 0:
            return JsonResponse({"code": 1, "message": "已存在同名项目"})

        # 创建新项目
        cursor.execute("""
            INSERT INTO project (projectName, projectType, projectIntro,foundationDate,teamId)
            VALUES (%s, %s,%s,%s,%s)
        """, [project_name, str(project_type), project_intro, foundation_date, int(team_id)])

        # 测试头像的部分
        cursor.execute('SELECT LAST_INSERT_ID() FROM project')
        project_id = cursor.fetchone()['LAST_INSERT_ID()']

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

        # 更新用户的 avatarId 字段
        cursor.execute(
                    'UPDATE project SET avatarId = %s WHERE projectId = %s',
                    [image_id, project_id]
        )
        # 测试头像结束
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
        cursor.execute("""
            UPDATE project
            SET projectName = %s, projectIntro = %s
            WHERE projectId = %s
        """, [new_project_name, new_project_intro, project_id])
        connection.commit()

    return JsonResponse({"code": 0, "message": "项目信息更新成功"})


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
        cursor.execute("""
            INSERT INTO tutorial (tutorialTime, tutorialTitle,tutorialTag,tutorialContent, projectId)
            VALUES (%s, %s, %s, %s, %s)
        """, [current_time, tutorial_title, tutorial_tag, tutorial_content, project_id])
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
        cursor.execute("""
            UPDATE tutorial
            SET tutorialTitle = %s, tutorialTag = %s, tutorialContent = %s
            WHERE tutorialId = %s
        """, [new_tutorial_title, new_tutorial_tag, new_tutorial_content, tutorial_id])
        connection.commit()

    return JsonResponse({"code": 0, "message": "教程信息更新成功"})


@csrf_exempt
def admin_delete_tutorial(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    tutorial_id = request_dict.get("tutorialId")
    connection = create_connection()

    with connection.cursor() as cursor:
        # 删除教程
        cursor.execute("DELETE FROM tutorial WHERE tutorialId = %s", [tutorial_id])
        connection.commit()

    return JsonResponse({"code": 0,
                         "message": "教程删除成功"})


@csrf_exempt
def admin_reply_question(request):
    request_dict = json.loads(request.body.decode('utf-8'))

    question_id = request_dict.get("questionId")  # 要回复的用户提问的question id
    user_id = request_dict.get("userId")  # 回复者的用户ID
    reply_content = request_dict.get("replyContent")  # 要回复的内容

    message_title = request_dict.get("message").get("title")
    message_content = request_dict.get("message").get("content")

    connection = create_connection()

    with connection.cursor() as cursor:
        # 插入新回复
        current_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
             INSERT INTO reply (postTime, postContent, posterId, replyToId)
             VALUES (%s, %s, %s, %s)
         """, [current_time, reply_content, user_id, question_id])

        # 查询receiver_id
        cursor.execute("SELECT posterId From question WHERE questionId = %s",[question_id])
        receiver_id = cursor.fetchone().get('posterId')

        # 发送回复提醒
        current_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('insert into message(messageTime,messageTitle,messageContent,messageIsRead,receiverId) '
                       'values (%s,%s,%s,%s,%s)', [current_time, message_title, message_content, 'False', receiver_id])
        connection.commit()

    return JsonResponse({"code": 0,
                         "message": "回复成功"})


@csrf_exempt
def admin_get_project_details(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    project_id = request_dict.get("projectId")
    connection = create_connection()

    with connection.cursor() as cursor:
        # 获取项目简介
        cursor.execute("SELECT projectIntro FROM project WHERE projectId = %s", [project_id])
        project_intro = cursor.fetchone()['projectIntro']

        # 获取项目的未回复 提问列表
        cursor.execute("""
            SELECT q.questionId, q.postTime, q.posterId,q.postContent, u.userName
            FROM unreplied_questions q
            JOIN user u ON q.posterId = u.userId
            WHERE q.projectId = %s
        """, [project_id])
        comments = [
            {"questionId": row['questionId'], "date": row['postTime'].strftime("%Y-%m-%d %H:%M"),
             "content": row['postContent'],
             "posterId": row['posterId'], "posterName": row['userName']} for
            row in cursor.fetchall()]

        # 获取教程列表
        cursor.execute("""
            SELECT tutorialId, tutorialTitle, tutorialContent, tutorialTime, tutorialTag
            FROM tutorial
            WHERE projectId = %s
        """, [project_id])
        tutorials = [
            {"id": row['tutorialId'], "title": row['tutorialTitle'], "content": row['tutorialContent'],
             "date": row['tutorialTime'].strftime("%Y-%m-%d"), "tag": row['tutorialTag']} for
            row in cursor.fetchall()]

        # 获取招募列表
        cursor.execute("""
            SELECT startTime,endTime,launchTime,dueTime,location, recruitmentType, volunteerHour, maximumNumber
            FROM recruitment
            WHERE projectId = %s
        """, [project_id])

        recruitments = [
            {
             "launchTime": row['launchTime'].strftime("%Y-%m-%d %H:%M"),
             "deadline": row['dueTime'].strftime("%Y-%m-%d %H:%M"),
             "startTime": row['startTime'].strftime("%Y-%m-%d %H:%M"),
             "endTime": row['endTime'].strftime("%Y-%m-%d %H:%M"),
             "location": row['location'], "type": row['recruitmentType'],
             "hours": row['volunteerHour'], "number": row['maximumNumber']} for row in cursor.fetchall()]
        connection.commit()

    return JsonResponse({
        "code": 0,
        "message": "获取项目信息成功",
        "projectIntro": project_intro,
        "comments": comments,
        "tutorials": tutorials,
        "recruitments": recruitments
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
        cursor.execute("""
                INSERT INTO question (postTime, postContent, projectId, posterId)
                VALUES (%s, %s, %s, %s)
            """, ((datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"),
                  post_content, project_id, user_id))
        connection.commit()
    return JsonResponse({"code": 0, "message": "提问成功"})


@csrf_exempt
def user_get_all_projects(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")

    connection = create_connection()
    # 获取用户所在的所有团队
    user_teams = set()
    with connection.cursor() as cursor:
        cursor.execute("SELECT teamId FROM team_member WHERE userId = %s", [user_id])
        for row in cursor.fetchall():
            user_teams.add(row['teamId'])

    # 查询所有项目及其相关信息，包括最后一次发布招募的时间
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.projectId, p.projectName, p.projectType, t.teamName, t.teamId, MAX(r.dueTime) as lastDueTime
            FROM project p
            JOIN team t ON p.teamId = t.teamId
            LEFT JOIN recruitment r ON p.projectId = r.projectId
            GROUP BY p.projectId, p.projectName, p.projectType, t.teamName, t.teamId
        """)
        projects = cursor.fetchall()

        project_list = []
        for project in projects:
            project_id = project["projectId"]
            project_name = project["projectName"]
            project_type = project["projectType"]
            team_name = project["teamName"]
            team_id = project["teamId"]
            last_due_time = project["lastDueTime"].strftime("%Y-%m-%d") if project["lastDueTime"] else "N/A"

            # 检查项目的团队是否是用户所在的团队
            is_my_team = team_id in user_teams

            project_list.append({
                "id": project_id,
                "name": project_name,
                "type": project_type,
                "team": team_name,
                "isMyTeam": is_my_team,
                "latestTime": last_due_time
            })
        connection.commit()

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
        # 查询是否已经收藏
        cursor.execute("SELECT COUNT(*) FROM user_favorite_project WHERE userId = %s And projectId = %s",
                       [user_id, project_id])
        result = cursor.fetchone()
        if result['COUNT(*)'] > 0:
            isCollect = True
        else:
            isCollect = False

        # 查询项目详细信息
        cursor.execute("SELECT projectName,projectType,projectIntro,teamId FROM project WHERE projectId = %s",
                       [project_id])
        result = cursor.fetchone()
        project_name = result.get('projectName')
        project_type = result.get('projectType')
        project_intro = result.get('projectIntro')

        # 查询项目所属队伍的名字
        team_id = result.get('teamId')
        cursor.execute("SELECT teamName FROM team WHERE teamId = %s", [team_id])
        result = cursor.fetchone()
        team_name = result.get('teamName')

        # 查询项目最后一次招募的时间
        cursor.execute("SELECT MAX(dueTime) AS lastDueTime FROM recruitment WHERE projectId = %s", [project_id])
        result = cursor.fetchone()
        last_due_time = result["lastDueTime"].strftime("%Y-%m-%d") if result["lastDueTime"] else "N/A"

        # 获取讨论区
        cursor.execute("SELECT questionPoster,questionTime,question,replyTime,reply FROM project_discussions WHERE "
                       "projectId = %s", [project_id])
        discussions = cursor.fetchall()
        discussion_list = []
        for discussion in discussions:
            question_poster = discussion['questionPoster']
            question_time = discussion['questionTime']
            question = discussion['question']

            reply_time = discussion['replyTime']
            reply = discussion['reply']
            discussion_list.append({
                "questionPoster": question_poster,
                "questionTime": question_time,
                "question": question,
                "replyTime": reply_time,
                "reply": reply
            })

        # 获取tutorial
        cursor.execute("SELECT tutorialTime,tutorialTitle,tutorialTag,tutorialContent FROM tutorial WHERE projectId = "
                       "%s", [project_id])
        tutorials = cursor.fetchall()
        tutorial_list = []
        for tutorial in tutorials:
            tutorial_time = tutorial['tutorialTime']
            tutorial_title = tutorial['tutorialTitle']
            tutorial_tag = tutorial['tutorialTag']
            tutorial_content = tutorial['tutorialContent']

            tutorial_list.append({
                "time": tutorial_time,
                "title": tutorial_title,
                "tag": tutorial_tag,
                "content": tutorial_content
            })

        connection.commit()
    discussion_list = sorted(discussion_list, key=lambda k: k['questionTime'])
    tutorial_list = sorted(tutorial_list, key=lambda k: k['tutorialTime'])

    return JsonResponse({
        "code": 0,
        "message": "获取特定团队的信息成功",
        "isCollect": isCollect,
        "projectName": project_name,
        "projectType": project_type,
        "projectIntro": project_intro,
        "latestTime": last_due_time,
        "teamId": str(team_id),
        "teamName": team_name,
        "discussionList": discussion_list,
        "tutorialList": tutorial_list
    }
    )


@csrf_exempt
def user_get_favorite_projects(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    user_id = request_dict.get("userId")

    connection = create_connection()
    with connection.cursor() as cursor:
        # 查询用户收藏的所有项目及其相关信息，包括最后一次招募的时间
        cursor.execute("""
            SELECT p.projectId, p.projectName, p.projectType, t.teamName, MAX(r.dueTime) as lastDueTime
            FROM user_favorite_project up
            JOIN project p ON up.projectId = p.projectId
            JOIN team t ON p.teamId = t.teamId
            LEFT JOIN recruitment r ON p.projectId = r.projectId
            WHERE up.userId = %s
            GROUP BY p.projectId, p.projectName, p.projectType, t.teamName
        """, [user_id])
        projects = cursor.fetchall()

        project_list = []
        for project in projects:
            project_id = project["projectId"]
            project_name = project["projectName"]
            project_type = project["projectType"]
            team_name = project["teamName"]
            last_due_time = project["lastDueTime"].strftime("%Y-%m-%d") if project[
                "lastDueTime"] else "N/A"

            project_list.append({
                "id": project_id,
                "name": project_name,
                "type": project_type,
                "team": team_name,
                "latestTime": last_due_time
            })
        connection.commit()

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
        # 检查项目是否已经在收藏夹中
        cursor.execute("SELECT COUNT(*) FROM user_favorite_project WHERE userId = %s AND projectId = %s",
                       [user_id, project_id])
        already_favorited = cursor.fetchone()['COUNT(*)'] > 0

        if already_favorited:
            # 如果已经收藏，则取消收藏
            cursor.execute("DELETE FROM user_favorite_project WHERE userId = %s AND projectId = %s",
                           [user_id, project_id])
            message = "项目已取消收藏"
        else:
            # 如果尚未收藏，则添加到收藏
            cursor.execute("INSERT INTO user_favorite_project (userId, projectId) VALUES (%s, %s)",
                           [user_id, project_id])
            message = "项目已添加到收藏"
        connection.commit()

    resp = {
        "code": 0,
        "message": message
    }
    return JsonResponse(resp)


@csrf_exempt
def upload_project_avatar(request):
    request_dict = json.loads(request.body.decode('utf-8'))
    project_id = request_dict.get("projectId")
    img = request.FILES["file"]

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

    print(img_path)
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'insert into image(imageName,imageURL) values (%s,%s)',
                [img_name, img_path]
            )

            cursor.execute('SELECT LAST_INSERT_ID()')
            image_id = cursor.fetchone()[0]

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
                return HttpResponse('')

            avatar_id = result['avatarId']

            # 查询头像的详细信息
            cursor.execute("SELECT imageURL FROM image WHERE imageId = %s", [avatar_id])
            avatar_info = cursor.fetchone()

            # 检查是否得到了imageURL
            if not avatar_info or not avatar_info['imageURL']:
                return HttpResponse('')

            image_path = avatar_info['imageURL']
            print(image_path)

            try:
                with open(image_path, 'rb') as f:
                    img = f.read()
                    img = base64.b64encode(img)
                return HttpResponse(img, content_type='image/jpeg')
            except IOError:
                # 图片文件不存在或无法打开
                return HttpResponse('Image not found', status=404)
