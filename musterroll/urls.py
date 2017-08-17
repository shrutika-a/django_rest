from django.conf.urls import url
from .views import FieldList,CategorySubCategoryDetail
urlpatterns=[
	url(r'^fieldList/$',FieldList.as_view()),
	url(r'^catSubCat/(?P<pk>[0-9]+)$',CategorySubCategoryDetail.as_view()),
]