from django.shortcuts import render , render_to_response , redirect
import json , re , requests
from django.http import JsonResponse
from function.crawler_cellphone import get_sogi_data
from django.db import connection

from web import models

#-----------------  page  -------------------

def base_page(request, pid=None ,del_pass=None):
	if 'username' in request.session:
		username = request.session['username']
	return render_to_response('index.html',locals())

def cell_phone(request):
	if 'username' in request.session:
		username = request.session['username']
	return render_to_response('cell_phone.html',locals())

def test(request):
	if 'username' in request.session:
		username = request.session['username']
	return render_to_response('test.html',locals())

def login_page(request):
	if 'username' in request.session:
		response = redirect('/')
	else :
		response = render_to_response('login.html',locals())
	return response

def register_page(request):
    return render_to_response("register.html",locals())

def logout_page(request):
	response = redirect('/')
	del request.session['username']
	return response

def error_page(request):
    return render_to_response("404_page.html",locals())

def setting_page(request):
	if 'username' in request.session:
		username = request.session['username']
	return render_to_response("setting.html",locals())

#----------------- function test ----------------

def getproductprice(request):
	#url = "https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=ASUS%20ZenFone%20Max%20Pro%20M2&page=1&sort=prc/dc"
    url = 'https://ecshweb.pchome.com.tw/search/v3.3/24h/results?q=zenfone&page=1&sort=prc/dc'

    res = requests.get(url)
    data = json.loads(res.text)
    webdata = data["prods"]

    projects = "<table class=\"table table-bordered dataTable\"> <thead> \
    <tr role=\"row\"> <th>名稱</th> <th>價格</th> </thead> <tbody>"
    for i in  webdata :
        if int(i["price"]) <5000 :
            break
        projects +="<tr role=\"row\">"
        projects +="<td>"+i["name"]+"</td>"
        projects +="<td>"+str(i["price"])+"</td>"
        projects +="</tr>"

    projects +="</tbody> </thead> </table>"

    return JsonResponse(projects,safe=False)

def getbutton(request):
	msg ='<div class=\"alert alert-danger\" style=\" margin-top:15px;\" role=\"alert\">'
	msg += '失敗 ! 請重新操作 ! '
	msg += '</div>'
	messag =  '失敗 ! 請重新操作 !帳號或密碼錯誤'

	return render(request , 'test.html' , {"msg":msg})

#-------------User function  ------------------

def sign_in(request):
	email = request.GET.get('email',None)
	password = request.GET.get('password',None)
	if password == '' or email == '':
		msg = '<div id = \"displayalert\"  class=\"alert alert-warning\" style=\" margin-top:15px;\" role=\"alert\">請輸入帳號密碼 !!</div>',
		resp = {
		'msg' : msg,
		'res' : 0  }
	else:
		try:
			user = models.User.objects.get(email=email)
			if user.password == password and user.email == email :
				request.session['username']= user.name
				request.session['useremail']= user.email
				resp = {
				'res' : 1 }
			else:
				msg = '<div id = \"displayalert\" class=\"alert alert-warning\" style=\" margin-top:15px;\" role=\"alert\">密碼錯誤，請重新確認 !!</div>'
				resp = {
				'msg' : msg ,
				'res' : 0 }
		except:
			msg = '<div id = \"displayalert\" class=\"alert alert-warning\" style=\" margin-top:15px;\" role=\"alert\">無此帳號，請重新輸入 !!</div>'
			resp = {
			'msg' : msg ,
			'res' : 0 }

	return  JsonResponse(resp,safe=False)


def sign_up(request):
	Name = request.GET.get('Name',None)
	Email = request.GET.get('Email',None)
	Password = request.GET.get('password',None)
	try :
		user = models.User.objects.get(email=Email)
		if user != '':
			msg = '<div id = \"displayalert\" class=\"alert alert-warning\" style=\" margin-top:15px;\" role=\"alert\">帳號已註冊 !!</div>'
			resp = {
			'msg' : msg ,
			'res' : 0 }
	except :
		models.User.objects.create(name=Name,email=Email,password=Password)
		resp = {
		'res' : 1
		}
	return JsonResponse(resp,safe=False)

def changePW(request):
	Password = request.POST['password']
	re_password = request.POST['re_password']
	if 'username' in request.session:
		change = models.User.objects.get(name=request.session['username'])
		change.password = Password
		change.save()
		messages.add_message(request, messages.SUCCESS, '密碼更新成功 !')
		msg ='<div class=\"alert alert-success\" style=\" margin-top:15px;\" role=\"alert\">密碼更新成功 ! </div>'
		response = redirect('/setting/')
	else:
		messages.add_message(request, messages.WARNING, '密碼更新失敗 ! 請重新操作 !')
		msg ='<div class=\"alert alert-success\" style=\" margin-top:15px;\" role=\"alert\">密碼更新失敗 ! 請重新操作 ! </div>'
		response = redirect('/setting/')
	return response

#------------- function  ------------------

def get_brands(request):
	with connection.cursor() as cursor:
		cursor.execute("select brands from main_brands")
		getdata=[item for item in cursor.fetchall()]
	connection.close()

	brand_data = ""
	for i in  range(len(getdata)) :
		brand_data += "<button style=\" margin-bottom:10px;\" class=\"btn btn-primary\" onclick=\"getdatatable(this)\" value=\""+getdata[i][0]+"\">"
		brand_data +="<td>"+getdata[i][0]+"</td>"
		brand_data +="</button> "

	return JsonResponse(brand_data,safe=False)

def get_phone_data (request):
	brand_name = request.GET.get('brand_name',None)

	with connection.cursor() as cursor:
		cursor.execute("select * from product where  brands_ID = (select id from main_brands where brands ='"+brand_name+"')")
		dbdata_detial=[item for item in cursor.fetchall()]
	connection.close()

	projects = "<table class=\"table table-bordered\" id=\"dataTable\" width=\"100%\" cellspacing=\"0\">\
	<thead><tr> <th>名稱</th> <th>price</th> <th>網址</th> </thead> <tbody>"
	for i in  dbdata_detial :
		projects +="<tr>"
		projects +="<td>"+i[2]+"</td>"
		projects +="<td>"+i[3]+"</td>"
		projects +="<td>"+i[4]+"</td>"
		projects +="</tr>"

	projects +="</tbody> </table> "

	return JsonResponse(projects,safe=False)

def get_new_celllp_data (request):
	USER_AGENT_VALUE = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36'
	query_url = 'https://www.sogi.com.tw'
	page_url = '/brands'

	setdata = get_sogi_data(USER_AGENT_VALUE,query_url,page_url)
	getdata = setdata.Get_brands_url()

	with connection.cursor() as cursor:
		cursor.execute("select brands from main_brands")
		dbdata_b=[item for item in cursor.fetchall()]
	connection.close()

	meg_act = 0
	with connection.cursor() as cursor:
		for i in range(len(getdata)):
			count = 0
			for j in range(len(dbdata_b)):
				if getdata[i][0] == dbdata_b[j][0]:
					count+=1
					break
			if count == 0 :
				meg_act +=1
				cursor.execute("insert into main_brands (brands , brands_url) value ('"+getdata[i][0]+"','"+getdata[i][1]+"')")
		connection.commit()
	connection.close()

	getdatadetial = setdata.Get_brands_products(getdata)

	with connection.cursor() as cursor:
		cursor.execute("select product_name from product")
		dbdata_p=[item for item in cursor.fetchall()]
	connection.close()

	with connection.cursor() as cursor:
		for i in range(len(getdatadetial)):
			count = 0
			for j in range(len(dbdata_p)):
				if getdatadetial[i][1] == dbdata_p[j][0]:
					count+=1
					break
			if count == 0 :
				meg_act +=1
				cursor.execute("insert into product (brands_ID , product_name , product_price , product_url) value\
				("+str(getdatadetial[i][0]+1)+",'"+getdatadetial[i][1]+"','"+getdatadetial[i][2]+"','"+getdatadetial[i][3]+"')")
		connection.commit()
	connection.close()
	if meg_act > 0:
		message = 'Data already update !!'
	else:
		message = "Data is lastest!!"

	return JsonResponse(message,safe=False)
