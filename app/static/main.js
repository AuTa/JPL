$(".kana").click(function() {
  $(this).toggleClass("positive");
});

$(".kana").hover(function() {
  $(this).toggleClass("positive negative");
}, function() {
  $(this).toggleClass("positive negative");
});

$(".sel-but").click(function() {
  var i = $(this).data("cell");
  var j = $(this).data("row");
  if (j === 0) {
    $(this).parents("table").find(".kana[data-cell='" + i + "'][data-row!='0']").toggleClass("positive");
  };
  if (i === 0) {
    $(this).parents("table").find(".kana[data-cell!='0'][data-row='" + j + "']").toggleClass("positive");
  };
});

$(".sel-but").hover(function() {
  var i = $(this).data("cell");
  var j = $(this).data("row");
  if (j === 0) {
    $(this).parents("table").find(".kana[data-cell='" + i + "'][data-row!='0']").toggleClass("hover");
  };
  if (i === 0) {
    $(this).parents("table").find(".kana[data-cell!='0'][data-row='" + j + "']").toggleClass("hover");
  };
});

$(".sel-but[data-cell='0'][data-row='0']").click(function() {
  $(this).parents("table").find(".kana").toggleClass("positive");
});

$(".sel-but[data-cell='0'][data-row='0']").hover(function() {
  $(this).parents("table").find(".kana").toggleClass("hover");
});

$(".sel-but[data-cell='0'][data-row='0']").dblclick(function() {
  $(this).parents("table").find(".kana").addClass("positive");
});

$(document).ready(function() {
    if (window.matchMedia('(min-width: 750px)').matches) {
        $(".tab-pane").addClass("active");
    } else {
        //...
    }
});
