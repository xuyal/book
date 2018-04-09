from django.db import models
from hashlib import sha1
from db.base_model import BaseModel

def get_hash(password):
	sh = sha1()
	sh.update(password.encode('utf8'))
	return sh.hexdigest()


class PassPortManger(models.Manager):
	'''添加一个用户信息'''
	def add_one_passport(self, username, password, email):
		passport = self.create(username=username, password=get_hash(password), email=email)
		return passport
	
	def get_one_passport(self, username, password):
		try:
			passport = self.get(username=username, password=get_hash(password))
		except Exception as e:
			passport = None
		return passport
	

class PassPort(BaseModel):
	'''用户模型类'''
	username = models.CharField(max_length=20, verbose_name='用户名称')
	password = models.CharField(max_length=40, verbose_name='用户密码')
	email = models.EmailField(verbose_name='用户邮箱')
	is_active = models.BooleanField(default=False, verbose_name='激活状态')
	# 用户表的管理器
	objects = PassPortManger()
	
	class Meta:
		db_table = 's_user_account'