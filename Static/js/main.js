// Custom Endpoint
var deleteComment = function (event) {
  var comment_id = event.currentTarget.value;
  $.post({
    type: "POST",
    url: "/comments/delete",
    data: {
      "comment_id": comment_id,
    },
    success(response) {
      var status = JSON.parse(response)["status"];
      if (status === "Comment Deleted") {
        location.reload();
      }
      else {
        error("comment-input");
      }
    }
  });
};

// Custom Endpoint
var createComment = function () {
  $.post({
    type: "POST",
    url: "/comments",
    data: {
      "username": $("#nameInput").val(),
      "email": $("#emailInput").val(),
      "comment": $("#commentInput").val()
    },
    success(response) {
      var status = JSON.parse(response)["status"];
      if (status === "Comment Successful") {
        location.reload();
      }
      else {
        error("comment-input");
      }
    }
  });
};


function error(type) {
  $("."+type).css("border-color", "#E14448");
}


$(document).ready(function () {
  $('.comment-delete-btn').on("click", deleteComment);
  $(document).on("click", "#submit-comment", createComment);
});