from django.shortcuts import render
import markdown
from . import util
import random


def convert_to_html(title):
    markdowner = markdown.Markdown()
    content = util.get_entry(title)
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = convert_to_html(title)
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html",
                      {
                          "title": title,
                          "entry": content
                      })


def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        content = convert_to_html(entry_search)
        if content is not None:
            return render(request, "encyclopedia/entry.html",
                          {
                              "title": entry_search,
                              "entry": content
                          })
        else:
            content = util.list_entries()
            newList = []
            for datas in content:
                if entry_search.lower() in datas.lower():
                    newList.append(datas)
            return render(request, "encyclopedia/results.html",
                          {
                              "entries": newList,
                          })


def new(request):
    if request.method == "POST":
        title = request.POST['title']
        text = request.POST['new_text']
        content = convert_to_html(title)
        if content is None:
            util.save_entry(title, text)
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })

        else:
            return render(request, "encyclopedia/error.html", {
                "message": "This entry already exists"
            })
    else:
        return render(request, "encyclopedia/new.html")


def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def randoms(request):
    titles = util.list_entries()
    title = random.choice(titles)
    content = convert_to_html(title)
    return render(request, "encyclopedia/entry.html",
                  {
                      "title": title,
                      "entry": content
                  })
