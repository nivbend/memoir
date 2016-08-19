function toggleLike(event) {
    event.preventDefault();
    var button = $(this);

    var action = "PUT";
    var toggle = function(response) {
        button.removeClass("btn-like").addClass("btn-unlike");
        button.removeClass("btn-default").addClass("btn-primary");
        button.find(".like-count").text(response.likers.length);
        button.trigger("likes_updated", [response.likers]);
    }

    if ($(this).hasClass("btn-unlike"))
    {
        action = "DELETE";
        toggle = function(response) {
            button.removeClass("btn-unlike").addClass("btn-like");
            button.removeClass("btn-primary").addClass("btn-default");
            button.find(".like-count").text(response.likers.length);
            button.trigger("likes_updated", [response.likers]);
        }
    }

    $.ajax({
        url: button.attr("url"),
        type: action,
        success: toggle,
        error: function(response) {
            if (403 == response.status) {
                alert("Must be logged in");
            }
        },
    });
}

$(document).ready(function() {
    $("button.btn-like, button.btn-unlike").click(toggleLike);
});
