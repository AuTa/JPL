$(".kana").not(".disable").click(function() {
  $(this).toggleClass("selected");
  var col = $(this).data("col");
  var row = $(this).data("row");
  var row_col = [[row, col]]
  var character = $(this).parents(".Table").data("character");
  var hiragana = $(this).parents(".Table").data("hiragana");
  $.ajax({
      url: $SCRIPT_ROOT + '/_ajax_state',
      type: "POST",
      data: JSON.stringify({"row_col": row_col, "character": character, "hiragana": hiragana}),
      contentType: "application/json; charset=utf-8",
    });
});

$(".kana").not(".disable").hover(function() {
  $(this).toggleClass("hover");
}, function() {
  $(this).toggleClass("hover");
});

$(".sel-but").click(function() {
  var col = $(this).data("col");
  var row = $(this).data("row");
  var character = $(this).parents(".Table").data("character");
  var hiragana = $(this).parents(".Table").data("hiragana");
  if (row === -1) {
    var sel = $(this).parents(".Table").find(".kana[data-col='" + col + "'][data-row!='-1']").not(".disable");
    sel.toggleClass("selected");
    var row_col = [];
    sel.each(function () {
      row_col.push([$(this).data("row"), col]);
    });
    $.ajax({
      url: $SCRIPT_ROOT + '/_ajax_state',
      type: "POST",
      data: JSON.stringify({"row_col": row_col, "character": character, "hiragana": hiragana}),
      contentType: "application/json; charset=utf-8",
    });
  };
  if (col === -1) {
    var sel = $(this).parents(".Table").find(".kana[data-col!='-1'][data-row='" + row + "']").not(".disable");
    sel.toggleClass("selected");
    var row_col = [];
    sel.each(function () {
      row_col.push([row, $(this).data("col")]);
    });
    $.ajax({
      url: $SCRIPT_ROOT + '/_ajax_state',
      type: "POST",
      data: JSON.stringify({"row_col": row_col, "character": character, "hiragana": hiragana}),
      contentType: "application/json; charset=utf-8",
    });
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
  var sel = $(this).parents(".Table").find(".kana").not(".disable");
  sel.toggleClass("selected");
  var character = $(this).parents(".Table").data("character");
  var hiragana = $(this).parents(".Table").data("hiragana");
  var row_col = [];
  sel.each(function () {
    row_col.push([$(this).data("row"), $(this).data("col")]);
  });
  $.ajax({
    url: $SCRIPT_ROOT + '/_ajax_state',
    type: "POST",
    data: JSON.stringify({"row_col": row_col, "character": character, "hiragana": hiragana}),
    contentType: "application/json; charset=utf-8",
  });
});

$(".sel-but[data-col='-1'][data-row='-1']").hover(function() {
  $(this).parents(".Table").find(".kana").not(".disable").toggleClass("hover");
});

$(".sel-but[data-col='-1'][data-row='-1']").dblclick(function() {
  $(this).parents(".Table").find(".kana").not(".disable").addClass("selected");
  var character = $(this).parents(".Table").data("character");
  var hiragana = $(this).parents(".Table").data("hiragana");
  var row_col = [[-1, -1]]
  $.ajax({
    url: $SCRIPT_ROOT + '/_ajax_state',
    type: "POST",
    data: JSON.stringify({"row_col": row_col, "character": character, "hiragana": hiragana}),
    contentType: "application/json; charset=utf-8",
  });
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
