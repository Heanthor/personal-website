/**
 * Created by reedtrevelyan on 8/21/16.
 */
$(function () {
    $("#main-gv-list").on('click', '.trash-button', function () {
        $(this).find(".delete-text").show(200);
        $(this).find(".glyphicon").hide();

        if ($(this).hasClass("btn-warning")) {
            deleteGroceryVisit($(this).parent().attr("id"));
        } else {
            $(this).addClass("btn-warning");
        }
    });
});

function deleteGroceryVisit(id) {
    $.ajax({
        url: "grocery_list/save_purchase",
        type: "POST",
        data: {
            "delete": "true",
            id: id
        },

        success: function () {
            $("#" + id).fadeOut(100);
        },

        error: function (xhr) {
            displayErrorXHR(xhr, "alert-danger");
        }
    })
}