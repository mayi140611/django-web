from django.http import HttpResponse
from rest_framework import viewsets
import json
from rest_framework.decorators import action
import dicproj.utils as utils
from dicproj.serializers import DicSerializer, CsvFileSerializer
from dicproj.models import Dic, CsvFile
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
import numpy as np


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

    @action(detail=False, methods=['POST'])
    def updateDic(self, request):
        """
        更新标注字典库
        :param request:
        {
            "updateDic":
                [
                    [
                        2,
                        "code1",
                        "name1",
                        "标准字典code1",
                        "标准字典name1",
                        -1
                    ],
                    [
                        2,
                        "code2",
                        "name2",
                        "标准字典code2",
                        "标准字典name2",
                        -1
                    ]
                ]
         }
        :return:
        """
        p = request.data
        print(p)
        d = {
            "head": {
                "code": 0,
                "msg": "success"
            },
            "body": {"result": []},
        }
        try:
            dft = pd.DataFrame(np.array(p['updateDic']))
            print(dft.head())
            # print(dft.info())
            utils.update_dic(dft)
        except Exception as e:
            print(e)
            d['head']['code'] = 1
            d['head']['msg'] = 'failure'
        return HttpResponse(json.dumps(d, ensure_ascii=False), content_type="application/json; charset=utf-8")


class Test2ViewSet(viewsets.GenericViewSet):
    queryset = CsvFile.objects.all()
    serializer_class = CsvFileSerializer
    parser_classes = (FormParser, MultiPartParser,)

    @action(detail=False, methods=['POST'])
    def match(self, request):
        """
        接收上传的csv文件，进行匹配，返回匹配结果
        :param request:
        :return:
        """
        # 文件上传
        file_obj = request.data["file"]
        dft = pd.read_csv(file_obj)
        print(dft.head())

        d = {
            "head": {
                "code": 0,
                "msg": "success"
            },
            "body": {"result": []},
        }
        try:
            rlist_match = []
            rlist_not_match = []
            for line in dft.itertuples():
                r = utils.match(line[1], line[2])
                # print(r)
                if not r:
                    continue
                if r[0] == 2:
                    rlist_not_match.extend(r[1])
                else:
                    rlist_match.append(r)
            # arr = np.array(rlist_not_match)
            # dft = pd.DataFrame(arr, columns=['status', 'code', 'name', 'match_code', 'match_name', 'match_flag'])
            d['body']['result'] = rlist_not_match
        except Exception as e:
            print(e)
            d['head']['code'] = 1
            d['head']['msg'] = 'failure'
        return HttpResponse(json.dumps(d, ensure_ascii=False), content_type="application/json; charset=utf-8")

