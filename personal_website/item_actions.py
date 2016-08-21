import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone, dateformat

from personal_website.models import Item


def delete_item_ajax(request):
    id_to_delete = request.POST.get("id")
    Item.objects.filter(pk=id_to_delete).delete()

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
    # check if item in db already
    try:
        tmp = Item.objects.get(name=item_name)

        # item is in db, update quantity
        response["add"] = "true"
        response["id"] = tmp.id
        current_quantity = tmp.quantity
        updated_quantity = int(current_quantity) + int(item_quantity)

        # update count
        Item.objects.filter(name=item_name).update(quantity=updated_quantity)
        response["item_quantity"] = updated_quantity
    except ObjectDoesNotExist:
        # object was not in db
        # create Item and save
        i = Item(name=item_name, quantity=item_quantity, date_added=date_added)
        i.save()
        response["id"] = i.id
    response["status"] = "Success"
    return response
