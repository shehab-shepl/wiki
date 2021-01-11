from django.shortcuts import render, redirect
from django import forms
from . import util
import secrets
from django.views.generic.edit import FormView

#for converting from markdown to html
import markdown2
from markdown2 import Markdown




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def show_entry(request , title):

    markdowner = Markdown()

    context = {
        "entries": markdowner.convert(util.get_entry(title)) ,
        "title": title
    }
    return render(request, "encyclopedia/title.html" ,context )

class add_form(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))

class edit_content(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))




def new_page(request):
    if request.method == 'POST':
        form = add_form(request.POST)



        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return redirect("/")
            else:
                return render(request, "encyclopedia/exist.html" , {"form" :add_form()} )

        else:
            context = {
                "form":form
            }
            return render(request, "encyclopedia/add.html",context  )

    else:
        
        return render(request, "encyclopedia/add.html" , {"form" :add_form()} )




def edit(request,title):
    if request.method == 'POST':
        newform = edit_content(request.POST)   
        if newform.is_valid():
            content = newform.cleaned_data["content"]
            title = title
            util.save_entry(title, content)
            return redirect("/") 
    else:
        
        context={
            "title" : title ,
            "form":edit_content() 
        }
        return render(request, "encyclopedia/edit.html" , context)
       




def search(request):
    markdowner = Markdown()
    search_result = []
    title = request.GET.get('q','')
    for entry in util.list_entries():
        if entry.lower()==title.lower():
            context = {
                "entries": markdowner.convert(util.get_entry(title)) ,
                "title": title
            }
            return render(request, "encyclopedia/title.html" ,context )
            
        else:
            if title.lower() in entry.lower():
                search_result.append(entry) 
                
    if len(search_result)>0:            
        return render(request, "encyclopedia/index.html",{"entries":search_result })
    else:
        return redirect("/")






def random(request):
    
    entries = util.list_entries()
    random_entry = secrets.choice(entries)
    context = {
        "entries": Markdown().convert(util.get_entry(random_entry) ) ,
        "title": random_entry
    }
    return render(request, "encyclopedia/title.html" ,context )