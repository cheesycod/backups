from django.shortcuts import render
from . import util
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django import forms
from django.utils.safestring import mark_safe
from django.db import models
import os
import markdown2
from random import randint
class WikiCreateForm(forms.Form):
    entry_name = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Type the name of your wiki entry here', "rows": 1, 'cols':90, 'style':"overflow:hidden;resize:none;"}))
    entry_content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Type the content of your wiki entry here', "cols": 89}), min_length=15)
    wiki_name = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Type the wiki name of your wiki entry here. This is usually the entry name but with underscores instead of spaces', "rows": 1, 'cols':90, 'style':"overflow:hidden;resize:none;"}))
    def check_wiki_name(self):
        if(self.cleaned_data["wiki_name"].__contains__(" ") or self.cleaned_data["wiki_name"].__contains__("\n")):
            return False
        return True
    def reserved(self):
        if(self.cleaned_data["wiki_name"].lower() == "admin" or self.cleaned_data["wiki_name"].lower() == "admin/"):
            return True
        return False
class SearchWikiForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

def search(request):
    if(request.method=="POST"):
        query_form = SearchWikiForm(request.POST)
        if(query_form.is_valid() == False):
            return HttpResponseBadRequest("Invalid")
        query = query_form.cleaned_data["query"]
        entry_list = util.list_entries()

        # Exact match
        if(query in entry_list):
            index = entry_list.index(query)
            return HttpResponseRedirect(entry_list[index])

        # Similar match
        similar_entry = []
        c = 0
        done = False
        for entry in entry_list:
            for i in entry:
                if(query.__contains__(i.lower()) or query.__contains__(i.upper())):
                    c+=1
                if(c > len(entry)/6 and not done and query[0].lower() == entry[0].lower()):
                    similar_entry.append(entry)
                    done = True
            c = 0
            done = False
        if(similar_entry == []):
            return render(request, "no_entries_found.html",{
                "name": query
            })
        similar_entry.sort()
        return render(request, 'encyclopedia/search_results.html', {
            "name": query,
            "entries": similar_entry
        })

    return render(request, "encyclopedia/search.html", {
        "form": SearchWikiForm()
    })

def index(request):
    entry_list = util.list_entries()
    entry_list.sort()
    return render(request, "encyclopedia/index.html", {
        "entries": entry_list
    })

def error(request, name):
    if(os.path.exists("encyclopedia/404.html")):
        return render(request, "encyclopedia/404.html", {})
    elif(os.path.exists("../encyclopedia/404.html")):
        return render(request, "../encyclopedia/404.html", {})
    else:
        return HttpResponseBadRequest("<strong>404</strong><br/><p>Not found</p>")
def create(request):
    if(request.method=="POST"):
        form = WikiCreateForm(request.POST)
        if(form.is_valid() == False):
            return render(request, "encyclopedia/500.html", {})
        if(form.check_wiki_name() == False):
            return render(request, "encyclopedia/invalid_wiki_name.html", {})
        if(form.reserved()):
            return render(request, "encyclopedia/invalid_wiki_name.html", {})
        entry_name = form.cleaned_data["entry_name"]
        entry_content = form.cleaned_data["entry_content"]
        wiki_name = form.cleaned_data["wiki_name"]
        md = open("entries/" + wiki_name + '.md', 'w')
        pcontent = "#" + entry_name + "\n" + entry_content
        md.write(pcontent)
        md.close()
        md = open("entries/" + wiki_name + '.md', 'r')
        html = open("entries/" + wiki_name + '.html', 'w')
        html.write(markdown2.markdown(md.read()))
        html.close()
        md.close()
        return render(request, "encyclopedia/done_submit.html", {
            "entry_name": entry_name
        })
    return render(request, "encyclopedia/create_new_page.html", {
        "form": WikiCreateForm()
    })
def delete(request):
    entry_list = util.list_entries()
    entry_list.sort()
    return render(request, "encyclopedia/delete_page.html", {
        "entries": entry_list
    })

def delcontent(request, name):
    if(os.path.exists("entries/" + name + ".md")):
        os.remove("entries/" + name + ".md")
    if(os.path.exists("entries/" + name + ".html")):
        os.remove("entries/" + name + ".html")
    return render(request, "encyclopedia/page_deleted.html", {
        "name": name
    })
def wiki(request, name):
    # Declare variables
    fnseed = "entries/" + name
    fn = fnseed + ".md"
    fnh = fnseed + ".html" 
    
    # Markdown
    if(name.__contains__('.md')):
        if(os.path.exists(fnseed)):
            md = open(fnseed, 'r')
            html = fnseed.strip(".md")
            return render(request, "encyclopedia/markdown.html", {
                "rmd": md.read(),
                })
        else:
            return render(request, "404.html", {})

    if(os.path.exists(fnh)):
        html = open(fnh, 'r')
        return render(request, "encyclopedia/entry.html", {
            "name": name,
            "content": html.read(),
        })
    elif(os.path.exists(fn)):
        md = open(fn, 'r')
        html = open(fnh, 'w')
        html_content = markdown2.markdown(md.read())
        html.write(html_content)
        return render(request, "encyclopedia/entry.html", {
            "name": name,
            "content": html.read(),
            })
    else:
        return render(request, "404.html", {})

def random(request):
    entry_list = util.list_entries()
    index = randint(0, len(entry_list) - 1)
    html = open("entries/" + entry_list[index] + ".html")
    return render(request, "encyclopedia/entry.html", {
        "name": entry_list[index],
        "content": html.read(),
    })
