from django.urls import include, path

from . import views

urlpatterns = [
   
    path('new/<uuid:league_id>/', views.GeneratePdf.as_view(), name="generate_pdf_report"),
    path('user_reports/', views.UserReportListView.as_view(), name="user_reports"),
    path('<uuid:report_id>/', views.PdfSuccess.as_view(), name="pdf_success"),
    path('<uuid:report_id>/delete/', views.ReportDeleteView.as_view(), name="report_delete"),
]