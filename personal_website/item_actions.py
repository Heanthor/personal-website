import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone, dateformat

from personal_website.models import Item


def delete_item_ajax(request):
    id_to_delete = request.POST.get("id")
    # don't actually delete item, tag it archived
    # this is so it can still be referenced by a grocery visit object later
    Item.objects.filter(pk=id_to_delete).update(archived=True)

    return {"status": "Success"}


def add_item_ajax(request):
    # ajax
    # extract from post
    item_name = request.POST.get("item_name")
    item_quantity = request.POST.get("item_quantity")
    date_added = timezone.now()
    date_added_str = dateformat.format(datetime.datetime.now(), 'F j, Y, P')
    response = {"item_name": item_name,
                "item_quantity": item_quantity,
                "date_added": date_added_str}

    # check if item in db already and is not archived
    results = Item.objects.filter(name=item_name).exclude(archived=True)

    if len(results) == 0:
        # object was not in db
        # create Item and save
        i = Item(name=item_name, quantity=item_quantity, date_added=date_added)
        i.save()
        response["id"] = i.id
    elif len(results) == 1:
        tmp = results[0]
        # item is in db, update quantity
        response["add"] = "true"
        response["id"] = tmp.id
        current_quantity = tmp.quantity
        updated_quantity = int(current_quantity) + int(item_quantity)

        # update count
        Item.objects.filter(name=item_name).update(quantity=updated_quantity)
        response["item_quantity"] = updated_quantity
    else:
        raise RuntimeError("PANIC")

    response["status"] = "Success"
    return response
