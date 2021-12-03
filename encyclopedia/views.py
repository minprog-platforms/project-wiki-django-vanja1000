from ctypes import get_errno
from django.shortcuts import render, redirect
from django.urls.base import reverse
import markdown2
from markdown2 import Markdown
from pygments.formatters import html
from . import util
from markdownify import markdownify
import random



markdown = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry):
    page = util.get_entry(entry)
    
    if page != None:
        html_page = markdown.convert(page)
        return render(request, "encyclopedia/entry_page.html", {
            "content": html_page,
            "title": entry
        })
    else:
        return render(request, "encyclopedia/ErrorPage.html", {
            "title": entry
        })
        
def search(request):
    all_entries = util.list_entries()

    search_term = request.GET.get('q')
    page = util.get_entry(search_term)  

    if page != None:
        html_page = markdown.convert(page)
        # return render(request, "encyclopedia/entry_page.html", {
        #     "content": html_page,
        #     "title": search_term
        # })
        # 
        return redirect("entry", search_term)          
        
    else:
        search_list = []
        for term in all_entries:
            if search_term.casefold() in term.casefold():
                search_list.append(term)
        
    #     return render(request, "encyclopedia/index.html", {
    #     "entries": search_list
    # })

        return redirect("index", search_list)

def new(request):
    if request.method == "POST":

        title = request.POST.get("title")
        print(title)
        content = request.POST.get("content")
    

        page = util.get_entry(title)

        if page != None:
            return render(request, "encyclopedia/already_exists.html", {
                "entry": title
            })

        else: 
            util.save_entry(title, content)
            page = util.get_entry(title)
            html_page = markdown.convert(page)
            
            return render(request, "encyclopedia/entry_page.html", {
                "content": html_page,
                "title": title
            })
           
    return render(request, "encyclopedia/new.html")


def edit(request, entry):
    content = util.get_entry(entry)

    if request.method == "GET":
  
        return render(request, "encyclopedia/edit.html", {
                "title": entry,
                "content": content
            })

    else:
        title = request.POST["title"]
        content = request.POST["content"]

        util.save_entry(title, content)

        page = util.get_entry(title)
        html_page = markdown.convert(page)

        return redirect("entry", title)


def random_entry(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)

    page = util.get_entry(random_entry)
    html_page = markdown.convert(page)

    return redirect("entry", random_entry)




