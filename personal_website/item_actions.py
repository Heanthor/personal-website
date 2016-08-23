import datetime
import json

from django.utils import timezone, dateformat

from personal_website.models import Item, GroceryVisit


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

    if item_name == "" or item_quantity == "" or int(item_quantity) > 50:
        return {"status": "Failure"}

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
        raise RuntimeError("Duplicate object %s" % results)

    response["status"] = "Success"
    return response


def add_grocery_list(request):
    response = {"status": "Success"}
    items_raw = json.loads(request.POST.get("items"))
    price_raw = request.POST.get("price")

    if len(items_raw) == 0 or price_raw == "":
        return {"status": "Failure"}

    items = map(int, items_raw)
    price = float(price_raw)

    print("Price in: %d, items in: %s" % (price, items))
    gv = GroceryVisit(price=price)
    gv.save()

    # update all items purchased in this grocery visit
    for item_id in items:
        # added to a gv, archive this item
        Item.objects.filter(id=item_id).update(grocery_visit=gv, archived=True)

    return response


def delete_grocery_list(request):
    id_to_remove = request.POST.get("id")
    GroceryVisit.objects.get(id=id_to_remove).delete()

    return {"status": "Success"}
