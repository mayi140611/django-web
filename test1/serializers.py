#!/usr/bin/python
# encoding: utf-8

"""
@author: Ian
@file: serializers.py
@time: 2019-04-30 15:04
"""
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')
