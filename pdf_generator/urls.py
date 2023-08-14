from django.urls import include, path

from . import views

urlpatterns = [
   
   #PDF generating view
    path('new/<uuid:league_id>/', views.GeneratePdf.as_view(), name="generate_pdf_report"),

    #List of user reports
    path('user_reports/', views.UserReportListView.as_view(), name="user_reports")
]