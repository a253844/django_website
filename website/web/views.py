from django.shortcuts import render
from django.shortcuts import render_to_response
import json , re , requests
from django.http import JsonResponse
from function.crawler_cellphone import get_sogi_data
# Create your views here.
def base_page(request):
	return render_to_response('base_page.html',locals())

def cell_phone(request):
	return render_to_response('cell_phone.html',locals())

def test(request):
	return render_to_response('test.html',locals())

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
    quary_data = request.GET.get('text',None)

    return JsonResponse(quary_data,safe=False)

def get_phone_data (request):
	USER_AGENT_VALUE = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36'
	query_url = 'https://www.sogi.com.tw'
	page_url = '/brands'

	setdata = get_sogi_data(USER_AGENT_VALUE,query_url,page_url)
	getdata = setdata.Get_brands_url()

	projects = "<table class=\"table table-bordered\" id=\"dataTable\" width=\"100%\" cellspacing=\"0\">\
	<thead><tr> <th>名稱</th> <th>網址</th> </thead> <tbody>"
	for i in  getdata :
		projects +="<tr>"
		projects +="<td>"+i[0]+"</td>"
		projects +="<td>"+i[1]+"</td>"
		projects +="</tr>"

	projects +="</tbody> </table> "

	return JsonResponse(projects,safe=False)
