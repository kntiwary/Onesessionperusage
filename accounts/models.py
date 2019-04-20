# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from datetime import datetime,timezone

from django.db import models

# Create your models here.
class LoggedInUser(models.Model):
    user = models.OneToOneField(User,related_name='logged_in_user',on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32,blank=True,null=True)
    token = models.CharField(max_length=63, blank=True, null=True)
    login_time= models.DateTimeField(default=datetime.now(timezone.utc))

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return
