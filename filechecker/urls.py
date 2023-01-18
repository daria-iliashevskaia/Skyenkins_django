from django.urls import path

from filechecker.views import FilesList, FileCreate, ShowFile, UpdateFile, DeleteFile

urlpatterns = [
    path('', FilesList.as_view(), name="home"),
    path('add_file/', FileCreate.as_view(), name="addfile"),
    path('detail_file/<int:pk>', ShowFile.as_view(), name="showfile"),
    path('update_file/<int:pk>', UpdateFile.as_view(), name="updatefile"),
    path('delete/<int:pk>', DeleteFile.as_view(), name="deletefile")

]
