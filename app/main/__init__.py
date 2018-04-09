from flask import Blueprint
main = Blueprint('main', __name__)


from . import views, errors
from ..models import Permission


# 上下文处理器，让变量在模板中全局可访问
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
