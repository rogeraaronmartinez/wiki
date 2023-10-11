from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import util
from django import forms
from django.urls import reverse
import random
import markdown2


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(), label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    check = util.get_entry(entry)
    if check == None:
        return render(request, "encyclopedia/error.html", {
            "error": "This page does not exist."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": markdown2.markdown(util.get_entry(entry)),
            "title": entry
        })

def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            check = util.get_entry(title)
            if check == None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('entry', kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/error.html", {
                    "error": "Duplicate Entry"
                })
    
    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm()
    })

def edit(request, title):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entry', kwargs={'entry': title} ))
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "form": NewEntryForm(initial={'title':title, 'content':content})
    })

def error(request):
    return render(request, "encyclopedia/error.html")

def random_entry(request):
    rand_entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('entry', kwargs={'entry':rand_entry}))

def search(request):
    if request.method == "GET":
        query = request.GET.get('q')
        if util.get_entry(query) is not None:
            return HttpResponseRedirect(reverse("entry", kwargs={'entry':query}))
        else:
            results = []
            for title in util.list_entries():
                if query.lower() in title.lower():
                    results.append(title)
    return render(request, "encyclopedia/search.html", {
        "entries":results,
        "query":query
    })

