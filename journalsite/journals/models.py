import datetime

from django.contrib import auth
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

# class User(auth.models.User, PermissionsMixin):
#     def __str__(self):
#         return "@{}".format(self.username)

from django.contrib.auth import get_user_model

User = get_user_model()

# @python_2_unicode_compatible
# class User(models.Model):
#     email_text = models.CharField('email', max_length=200)
#     password_hash = models.CharField('password', max_length=200)
#     def __str__(self):
#         return self.email_text
#
# @python_2_unicode_compatible

class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField('slug text', allow_unicode=True, unique=True)
    created_date = models.DateTimeField('date created', default= timezone.now)
    modified_date = models.DateTimeField('date modified', blank = True, null=True)
    name_text = models.CharField('journal name', max_length=200, unique=True)
    description_text = models.CharField('journal description', max_length=200)

    def __str__(self):
        return self.name_text

    def save(self, *args, **kwargs):
        # self.pk = self.pk
        # print("1111111&" + self.slug)
        self.slug = slugify(self.name_text)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # print("22222222&" + self.slug)
        return reverse("journals:single", kwargs={"slug":self.slug})

    class Meta:
        ordering = ["name_text"]
#
# @python_2_unicode_compatible
# EntryLog can record multiple users and journals
# class EntryLog(models.Model):
#     journal = models.ForeignKey(Journal,  related_name="user_journal", on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name="user_entry", on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.username
#
#     class Meta:
#         unique_together=("journal","user")


class Entry(models.Model):
    # user = models.ForeignKey(User, related_name="entries",on_delete=models.CASCADE)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    title_text = models.CharField('entry title', max_length=200)
    body_text = models.CharField('entry body', max_length=200)
    published_date = models.DateField('published date', default= datetime.date.today())
    hidden_boolean = models.BooleanField('hidden', default=False)
    deleted_boolean = models.BooleanField('deleted', default=False)
    orginal_entry = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField('replaced', default=True)
    def __str__(self):
        return self.title_text

    def get_absolute_url(self):
        print("********")
        return reverse("journals:entry_detail",kwargs={"entryname":self.title_text, "pk":self.pk })




    #
#
#
#
# @python_2_unicode_compatible
# class Entry(models.Model):
#     entry_log = models.ForeignKey(EntryLog, on_delete=models.CASCADE)
#     title_text = models.CharField('entry title', max_length=200)
#     body_text = models.CharField('entry body', max_length=200)
#     published_date = models.DateTimeField('published date')
#     hidden_boolean = models.BooleanField('hidden', default=False)
#     deleted_boolean = models.BooleanField('deleted', default=False)
#     def __str__(self):
#         return self.title_text

# @python_2_unicode_compatible
# class EntryHistoryActivity(models.Model):
#     entry_log = models.ForeignKey(EntryLog, on_delete=models.CASCADE)
#     pre_title_text = models.CharField('entry title', max_lengtph=200)
#     pre_body_text = models.CharField('entry body', max_length=200)
#     pre_published_date = models.DateTimeField('published date')
#     pre_hidden_boolean = models.BooleanField('hidden', default=False)
#     pre_deleted_boolean = models.BooleanField('deleted', default=False)
#     def __str__(self):
#         return self.title_text