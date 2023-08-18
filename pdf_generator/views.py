import datetime
from tempfile import NamedTemporaryFile

from django.contrib.auth import get_user_model
from django.core.files import File
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from google.cloud import storage

from stat_track.models import League, Player
from upload.models import Upload

from .models import Report
from .utils.pdf_process import html_to_pdf

User = get_user_model()

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        league = League.objects.get(pk=kwargs.get("league_id"))
        players_list = Player.objects.filter(leagues=league).order_by("last_name")
        date = datetime.date.today().strftime("%Y-%m-%d")

        open('templates/temp.html', "w").write(render_to_string('league_pdf.html', {'league':league, 'players_list': players_list, 'date': date}))

        # Converting the HTML template into a PDF file
        pdf = html_to_pdf('temp.html')
        
        # Save temporary pdf file and upload it to GCS as pdf file assigned to user_id so that multiple user can generate reports at once.
        with NamedTemporaryFile(mode='w+b') as temp:
            temp.write(pdf)
            temp.seek(0)

            with open(temp.name, 'rb') as saved_file:
                user_id = request.user.id

                # Creation of report.
                owned_reports_qs = request.user.reports.all()

                #If user already have temporary report, new file is assigned to temporary Report.
                if owned_reports_qs.filter(temporary=True):
                    report = owned_reports_qs.filter(temporary=True).first()
                    report.generated = date
                    report.pdf.save(f'rf_{report.pk}.pdf', saved_file)
                
                #If user have no reports, new report with 'temporary' field set to true is created
                else:
                    report = Report(league=league, owner=request.user, generated=datetime.date.today())
                    report.pdf.save(f'rf_{report.pk}.pdf', saved_file)
            temp.close()

        return redirect('pdf_success', report.id)
         

# View of newly generated Report
class PdfSuccess(DetailView):
    model = Report
    template_name = "pdf_generator/report_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self):
        return get_object_or_404(Report, pk=self.kwargs['report_id'])
    

# Managing user saved Reports
class UserReportListView(ListView):
    model = Report
    template_name = "pdf_generator/user_report_list.html"
    context_object_name = "report_list"

    def get_queryset(self):
        return self.request.user.reports.all()

class ReportDeleteView(
    DeleteView):
    model = Report
    template_name = "pdf_generator/report_delete.html"
    success_url = reverse_lazy("user_reports")

    def get_object(self):
        return get_object_or_404(Report, pk=self.kwargs['report_id'])