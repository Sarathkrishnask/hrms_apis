# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from uuid import uuid4

from django.core import validators
from django.db import models

from utils import validators as cust_validators


class UUIDModel(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Nameable(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Extendable(models.Model):
    # The Django convention is to use empty string '' (via blank=True) and not
    # NULL (via null=True) for string-based fields like CharField and TextField
    # to indicate that the field is not set. But given that this is the JSON
    # representation of an object, we expect to  show NULL in instances where
    # ext is not set in the API.
    ext = models.TextField(
        blank=True,
        null=True,
        validators=[cust_validators.validate_json_object_not_empty],
    )

    class Meta:
        abstract = True


class Notes(models.Model):
    notes = models.TextField(
        blank=True,
        max_length=4000,
        validators=[validators.MinLengthValidator(2)],
    )

    class Meta:
        abstract = True


class Resource(UUIDModel, Nameable, Notes):
    ts = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
