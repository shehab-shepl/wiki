from django.shortcuts import render, redirect
from django import forms
from . import util
import secrets
from markdown2 import Markdown
markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def show_entry(request , title):
    page_converted = markdowner.convert(util.get_entry(title)) 
    context = {
        "entries": page_converted,
        "title": title
    }
    return render(request, "encyclopedia/title.html" ,context )
