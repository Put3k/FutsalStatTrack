import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model

from stat_track.models import League, Player
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
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


# View of newly generated Report
class PdfView(View):
    def get(self, request, *args, **kwargs):
        pass

# Managing user saved Reports
class UserReportListView(ListView):
    model = Report
    template_name = "pdf_generator/user_report_list.html"
    context_object_name = "report_list"

    def get_queryset(self):
        return self.request.user.reports.all()