# from django.db import models
from mongoengine.fields import (BooleanField, DateTimeField, Document,
                                EmbeddedDocument, EmbeddedDocumentField,
                                IntField, ListField, StringField)


class Miner(Document):
    tid = StringField()
    name = StringField()
    handle = StringField()
    is_protected = BooleanField()
    follower_count = IntField()
    following_count = IntField()
    is_profile_image_set = BooleanField()
    last_updated = DateTimeField()

    meta = {"allow_inheritance": True}


class Status(Document):
    class User(EmbeddedDocument):
        tid = StringField()
        handle = StringField()

    tid = StringField()
    user = EmbeddedDocumentField(User)
    creationDate = DateTimeField()
    retweet_count = IntField()
    favourite_count = IntField()
    hashtags = ListField(StringField)

# class Tweeter(models.Model):
#     username = models.CharField(max_length=15)
#     company = models.CharField(max_length=48)
#     active = models.BooleanField()
#     records = models.PositiveIntegerField()


# class Tweet(models.Model):
#     tweeter = models.ForeignKey(Tweeter, on_delete=models.CASCADE)
#     comments = models.PositiveIntegerField()
#     reposts = models.PositiveIntegerField()
#     likes = models.PositiveIntegerField()
#     creationDate = models.DateField()
