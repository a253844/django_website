from django.test import TestCase

# Create your tests here.

from django.http import HttpResponse 
from catalog.models import Users
import hashlib
 
# 数据库操作
def testdb(request):
    admin = list(Users.objects.all().values())

    if(len(admin) < 1):
        addadmin = Users(username="admin",
                         password_hash=crypto_MD5("admin123456"),
                         email="admin@123.com",
                         user_type="admin",
                         is_enable="true")
        addadmin.save()
        return HttpResponse("<p>系統管理員，数据添加成功！</p>")
    return HttpResponse("<p>歡迎使用！</p>")

def crypto_MD5(str):
    crypto = hashlib.md5()
    crypto.update(str.encode('utf-8'))
    return crypto.hexdigest()
