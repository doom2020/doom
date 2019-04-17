from django.contrib import admin

# Register your models here.
from firm.models import *


admin.site.register(UserInfo)
admin.site.register(PDFInfo)
admin.site.register(JournalInfo)