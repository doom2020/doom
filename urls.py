from django.urls import path
from firm.views import *

urlpatterns = [
    path('', index_views, name='index'),
    path('register/', register_views, name='register'),
    path('login/', login_views, name='login'),
    path('upload/', upload_views, name='upload'),
    path('logout/', logout_views, name='logout'),
    path('check_register/', check_register_views, name='check_register'),
    path('code_create/', code_create_views, name='code_create'),
    path('pdf_to_txt/', pdf_to_txt_views, name='pdf2txt'),
    path('txt_to_csv/', txt_to_csv_views, name='txt2csv'),
    path('query_data/<int:page_num>', query_data_views, name='query_data'),
    path('feedback/', feedback_views, name='feedback'),
]