from django.contrib.auth.models import User
from test1.serializers import UserSerializer
from django.http import HttpResponse
from rest_framework import viewsets
import json
from rest_framework.decorators import action


class TestVeiwSet(viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def t1(self, request):
        """

        :param request:
        :return:
        """
        d = {
            "head": {
                "code": 1,
                "msg": "success"
            },
            "body": {"result": []},
        }
        return HttpResponse(json.dumps(d, ensure_ascii=False), content_type="application/json; charset=utf-8")

    @action(detail=False, methods=['POST'])
    def t2(self, request):
        """

        :param request:
        :return:
        """
        d = {
            "head": {
                "code": 1,
                "msg": "success"
            },
            "body": {"result": []},
        }
        return HttpResponse(json.dumps(d, ensure_ascii=False), content_type="application/json; charset=utf-8")


class TestVeiwSet1(viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def t1(self, request):
        """

        :param request:
        :return:
        """
        d = {
            "head": {
                "code": 1,
                "msg": "success"
            },
            "body": {"result": []},
        }
        return HttpResponse(json.dumps(d, ensure_ascii=False), content_type="application/json; charset=utf-8")
