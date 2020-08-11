from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name='miners'),
    path("add/", views.add, name="mineradd"),
    path("<int:minerid>/", views.manage, name="minemanage"),
    path("<int:minerid>/<str:minertitle>/",
         views.manage, name="minemanage-name"),
    path("search/", views.search, name="minersearch"),
    path("update/", views.update_mine, name="minerupdate")
]
