#!/usr/bin/python
# encoding: utf-8

"""
@author: Ian
@file: serializers.py.py
@time: 2019-04-30 12:23
"""
from rest_framework import serializers
from snippets.models import Snippet


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')