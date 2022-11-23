from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myaccount.models import UserProfile
import pandas as pd
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = '从一个excel文件的内容中读取用户列表，导入到数据库中'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        df = pd.read_excel(path)
        for i in range(len(df)):
            username = df['学号'][i]
            password = df['身份证后八位'][i]

            name = df['姓名'][i]
            identity_card = df['身份证后八位'][i]
            gender = df['性别'][i]
            telephone = df['手机号'][i]
            _class = df["班级"][i]
            political_status = df['政治面貌'][i]

            User.objects.create_user(
                username=username,
                password=password,
                first_name=name,
            )
            # 获取创建的用户在django自带用户系统中的id，后续外键绑定需要用到
            pk = User.objects.filter(username=username).first()
            UserProfile.objects.create(
                user=pk,
                name=name,
                identity_card=identity_card,
                gender=gender,
                telephone=telephone,
                classes=_class,
                political_status=political_status
            )
            logger.info('{} successful import'.format(name))
            logger.info('{}/{}'.format(i + 1, len(df)))
