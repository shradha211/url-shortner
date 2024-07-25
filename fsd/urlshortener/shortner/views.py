from shortner.forms import UrlForm
from django.shortcuts import render, redirect, get_object_or_404
from shortner.models import Url
import uuid

def generate_unique_short_url():
    while True:
        uid = str(uuid.uuid4())[:6]
        if not Url.objects.filter(short_url=uid).exists():
            return uid

def home(request):
    form = UrlForm()
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['original_url']
            if ("http://" not in link) and ("https://" not in link):
                link = "http://" + link 
            uid = generate_unique_short_url()
            new_url = Url(original_url=link, short_url=uid)
            new_url.save()
            context = {
                "uid": uid,
                "form": form
            }
            return render(request, 'final.html', context)
    context = {
        "form": form
    }
    return render(request, 'index.html', context)

def final(request, pk):
    url_details = get_object_or_404(Url, short_url=pk)
    return redirect(url_details.original_url)
