import datetime
from tempfile import NamedTemporaryFile

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from stat_track.models import League, Player
from upload.models import Upload

from .models import Report
from .utils.pdf_process import html_to_pdf

User = get_user_model()

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        league = League.objects.get(pk=kwargs.get("league_id"))
        players_list = Player.objects.filter(leagues=league).order_by("last_name")
        date = datetime.date.today().strftime("%d/%m/%Y")

        open('templates/temp.html', "w").write(render_to_string('league_pdf.html', {'league':league, 'players_list': players_list, 'date': date}))

        # Converting the HTML template into a PDF file
        pdf = html_to_pdf('temp.html')
        
        # Save temporary pdf file and upload it to GCS as pdf file assigned to user_id so that multiple user can generate reports at once.
        with NamedTemporaryFile(mode='w+b') as temp:
            temp.write(pdf)
            temp.seek(0)

            with open(temp.name, 'rb') as saved_file:
                user_id = request.user.id
                report = Report(league=league, owner=request.user, generated=datetime.date.today())
                report.pdf.save(f'rf_{report.pk}.pdf', saved_file)
                report.save()
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