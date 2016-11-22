from django.contrib import admin
from models import ALLBOOK
from models import BOOKTXT,BOOKUPDATA

class QuestionAdmin(admin.ModelAdmin):
    # ...
    list_display = ('question_text', 'pub_date', 'was_published_recently')

admin.site.register(ALLBOOK)
admin.site.register(BOOKTXT)
admin.site.register(BOOKUPDATA)
# Register your models here.
