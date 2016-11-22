from __future__ import unicode_literals
import uuid

from django.db import models

# Create your models here.

class ALLBOOK(models.Model):
    DD = 'd'
    BQ = 'b'
    source_card = (
        (DD, 'dindian'),
        (BQ, 'biqu'),
    )
    id = models.AutoField(primary_key=True)
    cid = models.UUIDField('book uuid',default=uuid.uuid4, editable=False,blank = False)
    name = models.CharField('book name',max_length=50,blank = False)
    source =  models.CharField(u'get source',max_length=5,choices=source_card,blank = False)
    # from django.utils import six, timezone
    creatime = models.DateTimeField('creat time',auto_now_add=True,editable=False)
    uptime = models.DateTimeField('up data time')

class BOOKTXT(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.UUIDField('book cid',blank = False)
    number = models.IntegerField('book zhang',blank = False)
    zname = models.CharField('book zhang name',max_length=50,blank = False)
    surl = models.URLField('source link url',blank = False)
    ztext = models.TextField('page text')
    creatime = models.DateTimeField('creat time',auto_now_add=True,editable=False)
    uptime = models.DateTimeField('up data time')

class BOOKUPDATA(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.UUIDField('book cid', blank=False)
    upinfo = models.CharField('updata info',max_length=200)
    gotime = models.DateTimeField('updata time',auto_now_add=True,editable=False)

