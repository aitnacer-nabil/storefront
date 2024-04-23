from django.urls import path
from . import views
urlpatterns = [
    path('products/',views.ProductApi.as_view()),
    path('product/',views.ProductApi.as_view()),
    path('product/<int:id>/',views.ProductApi.as_view()),
    path('collection/<int:pk>/',views.collection_detail, name='collection-detail'),
    path('collections/',views.collection_list),
    path('collection/',views.collection_save),

]
