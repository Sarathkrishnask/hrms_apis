# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 25


class MediumPageNumberPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 10000


class LargePageNumberPagination(PageNumberPagination):
    page_size = 50
    max_page_size = 10000
