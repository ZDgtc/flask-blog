from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


# 装饰器，用于判断当前用户是否具有指定权限，无则返回403
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorator_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
