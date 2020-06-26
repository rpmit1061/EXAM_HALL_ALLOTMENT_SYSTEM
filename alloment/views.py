from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .form import UploadForm
from .models import UploadFile
import os
# Create your views here.


def data_sheet_upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        sessionmonth = request.POST['sessionmonth']
        year = request.POST['year']
        if UploadFile.objects.filter(sessionmonth=sessionmonth, year=year).exists():
            resp_body = '<script>alert("For Selected Year and Session file is Already Uploaded");\
                                                            window.location="/alloment/data_sheet_upload"</script>'
            return HttpResponse(resp_body)
        else:
            if form.is_valid():
                form.save()
            resp_body = '<script>alert("Data Sheet Upload Successfully");\
                                                window.location="/alloment/data_sheet_upload"</script>'
            return HttpResponse(resp_body)
    else:
        form = UploadForm()
        alldata = UploadFile.objects.all()
        context = {'form': form, 'alldata': alldata}
        return render(request, 'data_sheet_upload.html', context)


def delete_record(request, ids=None):
        record = get_object_or_404(UploadFile, id=ids)
        if request.method == 'POST':
            file = request.POST['file']
            ttfile = request.POST['ttfile']
            if os.path.isfile(file):
                os.remove(file)
                os.remove(ttfile)
            record.delete()
        resp_body = '<script>alert("Record Deleted Successfully");\
                     window.location="/alloment/data_sheet_upload"</script>'
        return HttpResponse(resp_body)