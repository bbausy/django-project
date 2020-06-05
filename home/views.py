from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage
from photo.models import Category, Photo


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Category.objects.all()[:4]
    category = Category.objects.all()
    categoryPhoto = Category.objects.all()
    context = {'setting': setting,
               'page': 'home',
               'sliderdata': sliderdata,
               'category': category,
               'categoryPhoto': categoryPhoto}
    return render(request, 'index.html', context)


def about(request):
    setting=Setting.objects.get(pk=1)
    category = Category.objects.all()
    context={'setting': setting,
             'category': category,
             'page': 'about'}
    return render(request, 'about.html', context)


def contact(request):
    #mesajı göndermek için formu kaydetmek için

    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkürler.")
            return HttpResponseRedirect('/contact')

    #form için
    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'form': form}
    return render(request, 'contact.html', context)


def category_photos(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    photos = Category.objects.filter(category_id=id)
    context = {'photos': photos,
               'category': category,
               'categorydata': categorydata}
    return render(request, 'photos_s.html', context)