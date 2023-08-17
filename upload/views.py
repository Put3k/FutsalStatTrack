from django.http.response import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views import View
from django.http import FileResponse, Http404

from .models import Upload


class UploadView(View):
    
    def get(self, request):
        html="""
            <form method="post" enctype="multipart/form-data">
              <input type='text' style='display:none;' value='%s' name='csrfmiddlewaretoken'/>
              <input type="file" name="raport" accept="raport/*">
              <button type="submit">Upload Raport</button>
            </form>
        """ % (get_token(request))
        return HttpResponse(html)

    def post(self, request):
        file = request.FILES['raport']
        public_uri = Upload.upload_file(file, file.name)
        return HttpResponse("<embed src='%s' width='800px' height='2100px' />" % (public_uri))