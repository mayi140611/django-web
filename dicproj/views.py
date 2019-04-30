from django.contrib.auth.models import User
from test1.serializers import UserSerializer
from django.http import HttpResponse
from rest_framework import viewsets
import json
from rest_framework.decorators import action
import dicproj.utils as utils
from dicproj.serializers import DicSerializer, CsvFileSerializer
from dicproj.models import Dic, CsvFile
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
import pandas as pd

class TestVeiwSet(viewsets.GenericViewSet):
    queryset = Dic.objects.all()
    serializer_class = DicSerializer

    @action(detail=False, methods=['POST'])
    def standardize(self, request):
        """
        返回标准的(code, name)
        :param request:
            {
              "code": "string",
              "name": "string"
            }
        :return:
        """
        # p = json.loads(request.body.decode())
        p = request.data
        print(p)
        d = {
            "head": {
                "code": 0,
                "msg": "success"
            },
            "body": {"result": []},
        }
        if 'code' in p and 'name' in p:
            code = utils.standardize(p['code'])
            name = utils.standardize(p['name'])
            d['body']['result'] = (code, name)
        else:
            d['head']['code'] = 1
            d['head']['msg'] = 'failure'
        return HttpResponse(json.dumps(d, ensure_ascii=False), content_type="application/json; charset=utf-8")


class Test2ViewSet(viewsets.GenericViewSet):
    queryset = CsvFile.objects.all()
    serializer_class = CsvFileSerializer
    parser_classes = (FileUploadParser,)

    @action(detail=False, methods=['POST'])
    def match(self, request):
        """
        接收上传的csv文件，进行匹配，返回匹配结果
        :param request:
        :return:
        """
        p = request.data
        # file_obj = request.FILES.get('file', None)
        file_obj = request.data["file"]
        print(file_obj)#FileName.txt
        print(type(file_obj))#<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
        df = pd.read_csv(file_obj)#
        print(df.head())
        # print(file_obj.read().decode('utf8'))
        print(file_obj.name)#FileName.txt
        print(file_obj.size)#1544897
        print(p)#{'file': <InMemoryUploadedFile: FileName.txt (text/plain)>}
        d = {
            "head": {
                "code": 0,
                "msg": "success"
            },
            "body": {"result": []},
        }
        if 'code' in p and 'name' in p:
            code = utils.standardize(p['code'])
            name = utils.standardize(p['name'])
            d['body']['result'] = (code, name)
        else:
            d['head']['code'] = 1
            d['head']['msg'] = 'failure'
        return HttpResponse(json.dumps(d, ensure_ascii=False), content_type="application/json; charset=utf-8")