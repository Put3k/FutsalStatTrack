import datetime
from tempfile import NamedTemporaryFile

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View
from django.views.generic.base import TemplateView
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
        
        # Save temporary pdf file and upload it to GCS
        with NamedTemporaryFile(mode='w+b') as temp:
            temp.write(pdf)
            temp.seek(0)

            with open(temp.name, 'rb') as saved_file:
                file_uri = Upload.upload_file(saved_file, "temporary.pdf")
            temp.close()
        
         
         # rendering the template
        return HttpResponse("<embed src='%s' width='800px' height='2100px' />" % (file_uri))



# View of newly generated Report
class PdfSuccess(TemplateView):
    template_name = "report_success"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Data passed from pdf generator
        gcs_url = self.request.GET.get("gcs_url")
        owner = self.request.GET.get("owner")
        generated = self.request.GET.get("generated")
        league = self.request.GET.get("league")

        context["gcs_url"] = gcs_url
        context["owner"] = owner
        context["generated"] = generated
        context["league"] = league
        return context
    

# Managing user saved Reports
class UserReportListView(ListView):
    model = Report
    template_name = "pdf_generator/user_report_list.html"
    context_object_name = "report_list"

    def get_queryset(self):
        return self.request.user.reports.all()