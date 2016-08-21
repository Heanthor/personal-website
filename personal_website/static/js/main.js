$(function () {
    var ml = $("#main_list");

    // trash button animation
    ml.on('click', '.trash-button', function () {
        $(this).find(".delete-text").show(200);
        $(this).find(".glyphicon").hide();

        if ($(this).hasClass("btn-warning")) {
            // delete button is active, send delete request
            deleteEntry($(this).parent().attr("id"));
        } else {
            $(this).addClass("btn-warning");
        }
    });

    ml.on('click', '.log_reset', function () {
        grocery_visit();
    });


    ml.hoverIntent({
        over: function () {
            $(this).find(".text-muted").parent().fadeIn(100);
        },
        out: function () {
            $(this).find(".text-muted").parent().fadeOut(100);
        },
        selector: '.list-group-item'
    });


    // initialize popover
    $('#grocery_store').popover({
        html: true,
        content: function () {
            return $("#popover_content_wrapper").html();
        }
    });


    // close popover by clicking outside of box
    $(document).on('click', function (e) {
        $('[data-toggle="popover"],[data-original-title]').each(function () {
            //the 'is' for buttons that trigger popups
            //the 'has' for icons within a button that triggers a popup
            if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
                (($(this).popover('hide').data('bs.popover') || {}).inState || {}).click = false  // fix for BS 3.3.6
            }
        });
    });

    // Source: https://realpython.com/blog/python/django-and-ajax-form-submissions/
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    /*
     The functions below will create a header with csrftoken
     */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Submit post on submit
    $('#submit_form').on('submit', function (event) {
        event.preventDefault();
        addItem();
    });

    // AJAX for posting
    function addItem() {
        $.ajax({
            url: "grocery_list/", // the endpoint
            type: "POST", // http method
            data: {
                item_name: $.trim($('#item_input').val()),
                item_quantity: $('#quantity_input').val()
            }, // data sent with the post request

            // handle a successful response
            success: function (json) {
                $('#item_input').val(''); // remove the value from the input
                $('#quantity_input').val(1);
                console.log(json); // log the returned json to the console
                var name = json["item_name"];
                var quantity = json["item_quantity"];
                var dateAdded = json["date_added"];
                var id = json["id"];

                if (json["add"]) {
                    // change the quantity only
                    $("#" + id).find(".label").text(quantity);
                } else {
                    // add new list item
                    $("#main_list").append(
                        '<li class="list-group-item" id="' + id + '">\
                        <span class="label label-default">' + quantity + '</span>\
                        ' + name + '\
                        <button type="button" class="btn btn-xs pull-right trash-button" href="#{{ item.id }}">\
                            <span class="delete-text" hidden>Delete</span>\
                            <span class="glyphicon glyphicon-trash"></span>\
                        </button>\
                        <p style="padding-top: 5px" hidden>\
                            <span class="text-muted" style="padding-left: 1em">Added ' + dateAdded + '</span>\
                        </p>\
                    </li>')
                }
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                alert(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

    function deleteEntry(id) {
        $.ajax({
            url: "grocery_list/", // the endpoint
            type: "POST", // http method
            data: {
                delete: "true",
                id: id
            }, // data sent with the post request

            // handle a successful response
            success: function (json) {
                console.log(json);
                $("#" + id).fadeOut(100);
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                alert(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

    function grocery_visit() {
        var price = $("#price").val();
        var items = [];

        if (price == "") {
            return false;
        }

        // get all ids of items being purchased
        $(".grocery_item").each(function() {
            items.push($(this).attr("id"));
        });

        // send request
        $.ajax({
            url: "grocery_list/save_purchase", // the endpoint
            type: "POST", // http method
            data: {
                items: JSON.stringify(items),
                price: price
            }, // data sent with the post request

            // handle a successful response
            success: function (json) {
                console.log(json);
                $("#price").val("");
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                alert(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

    function removeAll() {
        $(".grocery_item").each(function () {
            deleteEntry($(this).attr("id"));
        });
    }
});
