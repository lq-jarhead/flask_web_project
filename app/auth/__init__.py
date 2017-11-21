# -*- coding: cp936 -*-
#定义author蓝本，用于用户验证系统
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
