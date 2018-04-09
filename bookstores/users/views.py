from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
import re
from users.models import PassPort


# Create your views here.
def register(request):
	return render(request, 'users/register.html')


def register_handle(request):
	'''进行用户注册处理'''
	#接收数据
	username = request.POST.get('user_name')
	password = request.POST.get('pwd')
	email = request.POST.get('email')
	#进行数据校验
	if not all([username, password, email]):
		return render(request, 'users/register.html',{'errmsg':'参数不能为空'})
	#判断邮箱是否合法
	if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
		return render(request, 'users/register.html', {'errmsg':'邮箱不合法'})
	passport = PassPort.objects.add_one_passport(username=username, password=password, email=email)
	return redirect(reverse('books:index'))


def login(request):
	'''显示登录界面'''
	username = ''
	checked = ''
	context = {
		'username': username,
		'checked': checked,
	}
	return render(request, 'users/login.html', context)


def login_check(request):
	'''进行用户登录校验'''
	# 1.获取数据
	username = request.POST.get('username')
	password = request.POST.get('pwd')
	remember = request.POST.get('remember')
	# 2.校验数据
	if not all([username, password, remember]):
		# 有数据为空
		return JsonResponse({'res': 2})
	# 3.进行处理:根据用户名和密码查找账户信息
	passport = PassPort.objects.get_one_passport(username=username, password=password)
	if passport:
		next_url = request.session.get('url_path', reverse('books:index'))
		jres = JsonResponse({'res':1,'next_url':next_url})
		#判断是否需要记住用户名
		if remember == 'true':
			jres.set_cookie('username',username,max_age=7*24*36)
		else:
			jres.delete_cookie('username')
			
		#记住用户的登录状态
		request.session['islogin'] = True
		request.session['username'] = username
		request.session['passport_id'] = passport.id
		return jres
	else:
		# 用户名或密码错误
		return JsonResponse({'res': 0})


def logout(request):
    '''用户退出登录'''
    # 清空用户的session信息
    request.session.flush()
    # 跳转到首页
    return redirect(reverse('books:index'))