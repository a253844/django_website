import json
from django.test import TestCase
from django.http import HttpResponse 
from catalog.models import Users
import hashlib
import datetime

 
# 数据库操作
def testdb(request):
    admin = list(Users.objects.all().values())

    if(len(admin) < 1):
        addadmin = Users(username="admin",
                         password_hash=crypto_MD5("admin123456"),
                         email="admin@123.com",
                         user_type="admin",
                         is_enable="true",
                         created_at=datetime.date.today()
                         )
        addadmin.save()
        return HttpResponse("<p>系統管理員，数据添加成功！</p>")
    return HttpResponse("<p>歡迎使用！</p>")

def crypto_MD5(str):
    crypto = hashlib.md5()
    crypto.update(str.encode('utf-8'))
    return crypto.hexdigest()

# 取得管理員
def getadmin(request):
    response = ""
    admin = Users.objects.filter(user_type="admin")
    for var in admin:
        response += var.username + " "

    return HttpResponse("<p>" + response + "</p>")

# 新增管理員
def createadmin(request):
    response = ""
    if(request.method == "POST"):
        postbody = request.body
        json_param = json.loads(postbody.decode())
        username = json_param.get('username','')
        user_type = json_param.get('user_type','')
        is_enable = json_param.get('is_enable','')
        email = json_param.get('email','')
        addadmin = Users(username=username,
                        password_hash=crypto_MD5("admin123456"),
                        email=email,
                        user_type=user_type,
                        is_enable=is_enable,
                        created_at=datetime.date.today()
                        )
        addadmin.save()
        response = "新增成功"

    return HttpResponse("<p>" + response + "</p>")

# 修改管理員訊息
def updateadmin(request):
    response = ''
    if(request.method == "POST"):
        postbody = request.body
        json_param = json.loads(postbody.decode())
        id = json_param.get('id','')
        username = json_param.get('username','')
        user_type = json_param.get('user_type','')
        is_enable = json_param.get('is_enable','')

        admin = Users.objects.filter(id=id)

        if(admin.count() == 0):
            response = "未找到使用者訊息"
            return HttpResponse("<p>" + response + "</p>")

        count = 0
        if(username != ''):
            admin.update(username = username)
            count += 1
        if(user_type != ''):
            admin.update(user_type = user_type)
            count += 1
        if(is_enable != ''):
            admin.update(is_enable = is_enable)
            count += 1
        if(count > 0 ):
            admin.update(update_at = datetime.date.today())
            response = "更新成功"

    return HttpResponse("<p>" + response + "</p>")

# 修改管理員密碼
def updateadminPassword(request):
    response = ''

    if(request.method == "POST"):
        postbody = request.body
        json_param = json.loads(postbody.decode())
        id = json_param.get('id','')
        Old_Password = json_param.get('Old_Password','')
        New_Password = json_param.get('New_Password','')

        admin = Users.objects.filter(id=id)
        if(admin.count() == 0):
            response = "未找到使用者訊息"
            return HttpResponse("<p>" + response + "</p>")

        if(admin[0].password_hash != crypto_MD5(Old_Password)):
            response = "舊密碼不一致"
            return HttpResponse("<p>" + response + "</p>")
        
        admin.update(password_hash = crypto_MD5(New_Password))
        response = "修改成功"

    return HttpResponse("<p>" + response + "</p>")

# 刪除管理員
def deleteadmin(request):
    response = ""
    if(request.method == "POST"):
        postbody = request.body
        json_param = json.loads(postbody.decode())
        id = json_param.get('id','')
        admin = Users.objects.filter(id=id)
        if(admin.count() == 0):
            response = "未找到使用者訊息"
            return HttpResponse("<p>" + response + "</p>")
        admin.delete()
        response = "刪除成功"

    return HttpResponse("<p>" + response + "</p>")