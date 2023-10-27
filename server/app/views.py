import pymysql
from django.http import HttpResponse
from django.http import JsonResponse
import json
from pymysql.cursors import DictCursor

"""
连接到数据库
"""


def create_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='123456',
                           database='userinfo',
                           charset='utf-8')


"""
- 用户部分
    
- 团队部分

- 项目部分

- 招募部分

- 综合部分
"""

"""
用户部分
"""


def volunteer_register_info(request):
    # 志愿者用户注册
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))

    college_id = request_dict["collegeId"]
    user_name = request_dict["userName"]
    password = request_dict["password"]
    email = request_dict["email"]
    telephone = request_dict["telephone"]
    user_type = "0"  # 0 代表普通志愿者

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'insert into user(collegeId,userName,password,email,telephone,userType) values(%s,%s,%s,%s,%s)',
                [college_id, user_name, password, email, telephone, user_type])
            connection.commit()

    return HttpResponse(None)


def admin_register_info(request):
    # 团队负责人注册
    assert request.method == "POST"
    request_dict = json.loads(request.body.decode('utf-8'))

    college_id = request_dict["collegeId"]
    user_name = request_dict["userName"]
    password = request_dict["password"]
    email = request_dict["email"]
    telephone = request_dict["telephone"]
    user_type = "1"  # 1 代表团队负责人

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('insert into user(collegeId,userName,password,email,telephone) values(%s,%s,%s,%s,%s)',
                           [college_id, user_name, password, email, telephone, user_type])
            connection.commit()

    return HttpResponse(None)


def login_info(request):
    # 用户登陆
    request_dict = json.loads(request.body.decode('utf-8'))
    college_id = request_dict["collegeId"]
    password = request_dict["password"]
    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("select * from user where collegeId = %s and password = %s", [college_id, password])
            is_match = cursor.fetchall()
            connection.commit()
            if len(is_match) == 1:
                resp = {"match": "true"}
                return JsonResponse(resp)
            else:
                resp = {"match": "false"}
                return JsonResponse(resp)


def get_user_info(request):
    if request.method != "GET":
        return HttpResponse("Method not allowed")

    # 获取请求中的collegeId参数
    college_id = request.GET.get("collegeId")
    if not college_id:
        return JsonResponse({"error": "Missing collegeId parameter"})

    # 连接数据库
    connection = create_connection()
    user_info = None
    with connection:
        with connection.cursor(DictCursor) as cursor:
            # 根据collegeId查询用户信息
            cursor.execute(
                'SELECT collegeId, userName,email, telephone,password,userType FROM user WHERE collegeId = %s',
                [college_id]
            )
            user_info = cursor.fetchone()
            connection.commit()

    # 检查是否找到了指定的用户
    if not user_info:
        return JsonResponse({"error": "User not found"})

    # 返回用户信息
    return JsonResponse(user_info)


def update_user_info(request):
    # 更新用户信息

    if request.method != "POST":
        return HttpResponse("Method not allowed")

    # 解析请求体中的JSON数据
    request_dict = json.loads(request.body.decode('utf-8'))

    # 获取用户信息
    college_id = request_dict.get("collegeId")
    new_password = request_dict.get("password")
    new_email = request_dict.get("email")
    new_telephone = request_dict.get("telephone")

    # 检查是否提供了所有必要的信息
    if not all([new_password, new_email, new_telephone]):
        return JsonResponse({"error": "Missing required fields"})

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            # 更新用户信息
            cursor.execute(
                'UPDATE user SET email = %s, telephone = %s, password = %s WHERE collegeId = %s',
                [new_email, new_telephone, new_password, college_id]
            )

            if cursor.rowcount == 0:
                return JsonResponse({"error": "User not found"})
            connection.commit()

    return JsonResponse({"success": True})


"""
团队信息部分
"""


def create_team(request):
    request_dict = json.loads(request.body.decode('utf-8'))

    # 获取团队注册信息
    team_name = request_dict.get("teamName")
    team_intro = request_dict.get("teamIntro")
    team_leader_id = request_dict.get("teamLeaderId")
    foundation_data = request_dict.get("foundationData")

    connection = create_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('insert into team(teamName,teamIntro,teamLeaderId,foundationData) values(%s,%s,%s,%s,%s)',
                           [team_name, team_intro, team_leader_id, foundation_data])
            connection.commit()

    return HttpResponse(None)


def get_team_info(request):
    if request.method != "GET":
        return HttpResponse("Method not allowed")

    team_id = request.GET.get("teamId")
    if not team_id:
        return JsonResponse({"error": "Missing teamId parameter"})

    connection = create_connection()

    team_info = None
    with connection:
        with connection.cursor(DictCursor) as cursor:
            # teamId
            cursor.execute(
                'SELECT teamId, teamName,teamIntro, teamLeaderId FROM team WHERE teamId = %s',
                [team_id]
            )
            team_info = cursor.fetchone()
            connection.commit()

    if not team_info:
        return JsonResponse({"error": "Team not found"})

    return JsonResponse(team_info)

def apply_team(request):


    team_id = request.GET.get("teamId")