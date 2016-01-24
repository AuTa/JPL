$(".kana").not(".disable").click(function() {
  $(this).toggleClass("selected");
  var i = $(this).data("col");
  var j = $(this).data("row");
  var character = $(this).parents(".Table").data("character");
  var hiragana = $(this).parents(".Table").data("hiragana");
  var state = {"state": [[character, j, i, hiragana]]};
  console.dir(state);
  $.getJSON($SCRIPT_ROOT + '/_ajax_state', {"col": i, "row": j, "character": character, "hiragana": hiragana});
});

$(".kana").not(".disable").hover(function() {
  $(this).toggleClass("hover");
}, function() {
  $(this).toggleClass("hover");
});

$(".sel-but").click(function() {
  var i = $(this).data("col");
  var j = $(this).data("row");
  if (j === -1) {
    $(this).parents(".Table").find(".kana[data-col='" + i + "'][data-row!='-1']").not(".disable").toggleClass("selected");
  };
  if (i === -1) {
    $(this).parents(".Table").find(".kana[data-col!='-1'][data-row='" + j + "']").not(".disable").toggleClass("selected");
  };
});

$(".sel-but").hover(function() {
  var i = $(this).data("col");
  var j = $(this).data("row");
  if (j === -1) {
    $(this).parents(".Table").find(".kana[data-col='" + i + "'][data-row!='-1']").not(".disable").toggleClass("hover");
  };
  if (i === -1) {
    $(this).parents(".Table").find(".kana[data-col!='-1'][data-row='" + j + "']").not(".disable").toggleClass("hover");
  };
});

$(".sel-but[data-col='-1'][data-row='-1']").click(function() {
  $(this).parents(".Table").find(".kana").not(".disable").toggleClass("selected");
});

$(".sel-but[data-col='-1'][data-row='-1']").hover(function() {
  $(this).parents(".Table").find(".kana").not(".disable").toggleClass("hover");
});

$(".sel-but[data-col='-1'][data-row='-1']").dblclick(function() {
  $(this).parents(".Table").find(".kana").not(".disable").addClass("selected");
});

$("form").submit(function(e){
  var submit_time = new Date();
  submit_time_utc = submit_time.toUTCString();
  document.getElementById("submit_time").value = submit_time_utc;
});


$(document).ready(function() {
    if (window.matchMedia('(min-width: 750px)').matches) {
        $(".tab-pane").addClass("active");
    } else {
        //...
    };
});
