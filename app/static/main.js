$(".kana").click(function() {
  $(this).toggleClass("selected");
});

$(".kana").hover(function() {
  $(this).toggleClass("hover");
}, function() {
  $(this).toggleClass("hover");
});

$(".sel-but").click(function() {
  var i = $(this).data("cell");
  var j = $(this).data("row");
  if (j === 0) {
    $(this).parents(".Table").find(".kana[data-cell='" + i + "'][data-row!='0']").toggleClass("selected");
  };
  if (i === 0) {
    $(this).parents(".Table").find(".kana[data-cell!='0'][data-row='" + j + "']").toggleClass("selected");
  };
});

$(".sel-but").hover(function() {
  var i = $(this).data("cell");
  var j = $(this).data("row");
  if (j === 0) {
    $(this).parents(".Table").find(".kana[data-cell='" + i + "'][data-row!='0']").toggleClass("hover");
  };
  if (i === 0) {
    $(this).parents(".Table").find(".kana[data-cell!='0'][data-row='" + j + "']").toggleClass("hover");
  };
});

$(".sel-but[data-cell='0'][data-row='0']").click(function() {
  $(this).parents(".Table").find(".kana").toggleClass("selected");
});

$(".sel-but[data-cell='0'][data-row='0']").hover(function() {
  $(this).parents(".Table").find(".kana").toggleClass("hover");
});

$(".sel-but[data-cell='0'][data-row='0']").dblclick(function() {
  $(this).parents(".Table").find(".kana").addClass("selected");
});

$(document).ready(function() {
    if (window.matchMedia('(min-width: 750px)').matches) {
        $(".tab-pane").addClass("active");
    } else {
        //...
    }
});
