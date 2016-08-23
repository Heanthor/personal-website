from __future__ import print_function

import json
from collections import OrderedDict

from django.http import HttpResponse
from django.shortcuts import render

from forms import AddItemForm
from models import Item, GroceryVisit

from personal_website.item_actions import delete_item_ajax, add_item_ajax, add_grocery_list, delete_grocery_list
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def index(request):
    return HttpResponse(render(request, "personal_website/index.html"))


@require_http_methods(["POST"])
def sign_up(request):
    print(request.POST.get("email"))
    print(request.POST.get("password"))


@require_http_methods(["POST"])
def log_in(request):
    pass


def grocery_list(request):
    if request.method == "POST":
        if request.POST.get("delete"):
            response = delete_item_ajax(request)
            return HttpResponse(json.dumps(response),
                                content_type="application/json")
        else:
            response = add_item_ajax(request)
            return HttpResponse(json.dumps(response),
                                content_type="application/json")
    else:
        # normal page load
        # only show items that are active
        items_list = Item.objects.filter(archived=False).order_by('date_added')
        form = AddItemForm()

        context = {
            "items_list": items_list,
            "form": form,
        }

        return render(request, "personal_website/grocery_list.html", context)


def grocery_visits(request):
    visit_items = OrderedDict()

    for v in GroceryVisit.objects.all().order_by('-date_added'):
        visit_items[v] = Item.objects.filter(grocery_visit=v)

    return HttpResponse(render(request, "personal_website/grocery_visits.html", {"data": visit_items.iteritems()}))


@require_http_methods(["POST"])
def save_purchase(request):
    if request.POST.get("delete"):
        response = delete_grocery_list(request)
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = add_grocery_list(request)
        return HttpResponse(json.dumps(response), content_type="application/json")

