from django.urls import include, path

from . import views

urlpatterns = [
   
   #PDF generating view
    path('new/<uuid:league_id>/', views.GeneratePdf.as_view(), name="generate_pdf_report"),
]