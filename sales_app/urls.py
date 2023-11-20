from django.urls import path,include
from sales_app  import views


urlpatterns = [
    path('',views.first,name="first"),
    
]
