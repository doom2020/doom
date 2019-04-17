from django.db import models
import datetime

# Create your models here.

class UserInfoManager(models.Manager):
    def get_queryset(self):
        return super(UserInfoManager, self).get_queryset().filter(isdelete=False)


# 用户表
class UserInfo(models.Model):
    user_obj = UserInfoManager()
    uname = models.CharField(max_length=25, verbose_name='用户姓名', null=False)
    upwd = models.CharField(max_length=60, verbose_name='用户密码', null=False)
    uphone = models.CharField(max_length=25, verbose_name='用户手机', null=False)
    uemail = models.EmailField(verbose_name='用户邮箱', null=False)
    isdelete = models.BooleanField(default=False, verbose_name='删除用户')

    def __str__(self):
        return self.uname

    class Meta:
        db_table = "userinfo"
        verbose_name = "userinfo"
        verbose_name_plural = verbose_name
        ordering = ["id"]

    @classmethod
    def create_user(cls, uname, upwd, uphone, uemail, isdelete=False):
        new_user = cls(uname=uname, upwd=upwd, uphone=uphone, uemail=uemail, isdelete=isdelete)
        return new_user


class PDFInfoManager(models.Manager):
    def get_query(self):
        return super(PDFInfoManager, self).get_queryset().filter(isdelete=False)


class PDFInfo(models.Model):
    pdf_obj = PDFInfoManager()
    title = models.CharField(max_length=100, verbose_name='期刊标题', null=False)
    author = models.CharField(max_length=50, verbose_name='作者姓名', null=False)
    position = models.CharField(max_length=250, verbose_name='作者职位', null=True)
    email = models.EmailField(verbose_name='联系邮箱', null=False)
    file_name = models.CharField(max_length=60, verbose_name='文件名', null=True)
    # data_time = models.DateTimeField(auto_created=True, default="time", verbose_name='创建时间')
    # isdelete = models.BooleanField(default=False, verbose_name='删除数据')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "pdfinfo"
        verbose_name = "pdfinfo"
        verbose_name_plural = verbose_name
        ordering = ["id"]

    @classmethod
    def create_data(cls, title, author, position, email, file_name, data_time, isdelete=False):
        new_pdf = cls(title=title, author=author, position=position, email=email, file_name=file_name, data_time=data_time, isdelete=isdelete)
        return new_pdf


class JournalInfoManager(models.Manager):
    def get_query(self):
        return super(JournalInfoManager, self).get_queryset().all()


class JournalInfo(models.Model):
    journal_obj = JournalInfoManager()
    classify = models.CharField(max_length=100, verbose_name="期刊类型", null=False)
    title = models.CharField(max_length=100, verbose_name='期刊标题', null=False)
    author = models.CharField(max_length=50, verbose_name='作者姓名', null=False)
    position = models.CharField(max_length=250, verbose_name='作者职位', null=True)
    email = models.EmailField(verbose_name='联系邮箱', null=False)
    # data_time = models.DateTimeField(auto_created=True, default="time", verbose_name='创建时间')
    # isdelete = models.BooleanField(default=False, verbose_name='删除数据')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "journalinfo"
        verbose_name = "journalinfo"
        verbose_name_plural = verbose_name
        ordering = ["id"]

    @classmethod
    def create_data(cls, classify, title, author, position, email, data_time, isdelete=False):
        new_journal = cls(classify=classify, title=title, author=author, position=position, email=email, data_time=data_time, isdelete=isdelete)
        return new_journal

