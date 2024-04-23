from django.urls import path
from . import views
urlpatterns = [
    path('products/',views.product_list),
    path('product/',views.product_save),
    path('product/<int:id>/',views.product_detail),
    path('collection/<int:pk>/',views.collection_detail, name='collection-detail'),
    path('collections/',views.collection_list),
    path('collection/',views.collection_save),

]
