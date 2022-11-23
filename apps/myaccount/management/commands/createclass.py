from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Settings.models import ClassType
import pandas as pd


class Command(BaseCommand):
    help = '从一个excel文件的内容中读取班级列表，写入数据库'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        df = pd.read_excel(path)
        for i in range(len(df)):
            class_name = df['班级'][i]
            class_teacher = df['分管辅导员'][i]

            ClassType.objects.create(
                class_name=class_name,
                class_teacher=class_teacher,
            )
            print('{} successful import'.format(class_name))
            print('{}/{}'.format(i, len(df)))
