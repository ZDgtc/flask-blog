from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, ValidationError
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField("真实姓名", validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('个性签名')
    submit = SubmitField('提交修改')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email])
    username = StringField('用户名', validators=[Required(), Length(1, 64), Regexp('[A-Za-z0-9_.]*', 0,
                                                                                '用户名必须由字母、数字和下划线组成')])
    confirmed = BooleanField('已确认')
    # 下拉列表，实例必须在choices中设置各选项，coerce将标识符id从字符串转化为整数
    role = SelectField('角色', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('个性签名')
    submit = SubmitField('提交修改')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        # 选项必须由两个元素的元组构成：标识符和文本字符串
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    # 检查值是否发生变化，且新值不能与其他用户相应字段的值重复，若无变化，跳过验证
    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被注册')
