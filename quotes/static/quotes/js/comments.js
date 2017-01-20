function showEditForm(event, link) {
  event.preventDefault();

  var comment_pk = link.data("pk");

  if (link.data("display")) {
    $("#comment_" + comment_pk + "_detail").addClass("hidden");
    $("#comment_" + comment_pk + "_edit").removeClass("hidden");
  }
  else {
    $("#comment_" + comment_pk + "_detail").removeClass("hidden");
    $("#comment_" + comment_pk + "_edit").addClass("hidden");
  }
}

function addComment(event) {
  event.preventDefault();

  text_source = $(event.target).data('source');

  $.ajax({
    url: $(event.target).attr("action"),
    method: "POST",
    data: {
      text: $(text_source).val(),
    },
    success: function (response) {
      location.hash = "#comment_" + response.comment_pk;
      location.reload();
    },
    error: function (response) {
      if (400 == response.status) {
        alert("Comment must have content");
        $(text_source).focus();
        return;
      }
      if (403 == response.status) {
        alert("Must be logged in");
        return;
      }
    }
  });
}

function editComment(event, link) {
  event.preventDefault();

  var comment_pk = link.data("pk");

  $.ajax({
    url: link.data("url"),
    type: link.data("method"),
    data: {
      text: $("#comment_" + comment_pk + "_text").val()
    },
    success: function(response) {
      $("#comment_" + comment_pk + "_detail").removeClass("hidden");
      $("#comment_" + comment_pk + "_edit").addClass("hidden");

      location.hash = "#comment_" + comment_pk;
      location.reload();
    },
    error: function(response) {
      if (400 == response.status) {
        alert("Comment must have content");
        $("#comment_" + comment_pk + "_text").focus();
        return;
      }
      if (403 == response.status) {
        alert("Must be logged in");
        return;
      }
    }
  });
}

function deleteComment(event, link) {
  event.preventDefault();

  if (!confirm("Delete comment?")) {
    return;
  }

  $.ajax({
    url: link.data("url"),
    type: link.data("method"),
    success: function(response) {
      // Reload at top of page.
      location.hash = "";
      location.reload();
    },
    error: function(response) {
      if (403 == response.status) {
        alert("Must be logged in");
      }
    }
  });
}
