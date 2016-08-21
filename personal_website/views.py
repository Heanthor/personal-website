from __future__ import print_function

import json

from django.http import HttpResponse
from django.shortcuts import render

from forms import AddItemForm
from models import Item, GroceryVisit

from personal_website.item_actions import delete_item_ajax, add_item_ajax
from django.views.decorators.http import require_http_methods


def index(request):
    return HttpResponse(render(request, "personal_website/index.html"))


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
        items_list = Item.objects.order_by('date_added')
        form = AddItemForm()

        context = {
            "items_list": items_list,
            "form": form,
        }

        return render(request, "personal_website/grocery_list.html", context)


@require_http_methods(["POST"])
def save_purchase(request):
    response = {"status": "Success"}
    items = map(int, json.loads(request.POST.get("items")))
    price = float(request.POST.get("price"))

    print ("Price in: %d, items in: %s" % (price, items))
    gv = GroceryVisit(price=price)
    gv.save()

    # update all items purchased in this grocery visit
    for item_id in items:
        Item.objects.filter(id=item_id).update(grocery_visit=gv)

    return HttpResponse(json.dumps(response), content_type="application/json")
