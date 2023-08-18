from django.urls import include, path

from . import views

urlpatterns = [
   
    #PDF generating
    path('new/<uuid:league_id>/', views.GeneratePdf.as_view(), name="generate_pdf_report"),

    #List of user reports
    path('user_reports/', views.UserReportListView.as_view(), name="user_reports"),

    #PDF Detail View
    path('<uuid:report_id>/', views.PdfSuccess.as_view(), name="pdf_success"),
]