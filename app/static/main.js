$(".kana").not(".disable").click(function() {
  $(this).toggleClass("selected");
  var col = $(this).data("col");
  var row = $(this).data("row");
  var character = $(this).data("character");
  var hiragana = $(this).parents(".Table").data("hiragana");
  var chara_row_col_hira = [[character, [row, col, hiragana]]];
  $.ajax({
      url: $SCRIPT_ROOT + '/_ajax_state',
      type: "POST",
      data: JSON.stringify({"chara_row_col_hira": chara_row_col_hira}),
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
  var hiragana = $(this).parents(".Table").data("hiragana");
  if (row === -1) {
    var sel = $(this).parents(".Table").find(".kana[data-col='" + col + "'][data-row!='-1']").not(".disable");
    sel.toggleClass("selected");
    var chara_row_col_hira = [];
    sel.each(function () {
      chara_row_col_hira.push([$(this).data("character"), [$(this).data("row"), col, hiragana]]);
    });
    $.ajax({
      url: $SCRIPT_ROOT + '/_ajax_state',
      type: "POST",
      data: JSON.stringify({"chara_row_col_hira": chara_row_col_hira}),
      contentType: "application/json; charset=utf-8",
    });
  };
  if (col === -1) {
    var sel = $(this).parents(".Table").find(".kana[data-col!='-1'][data-row='" + row + "']").not(".disable");
    sel.toggleClass("selected");
    var chara_row_col_hira = [];
    sel.each(function () {
      chara_row_col_hira.push([$(this).data("character"), [row, $(this).data("col"), hiragana]]);
    });
    $.ajax({
      url: $SCRIPT_ROOT + '/_ajax_state',
      type: "POST",
      data: JSON.stringify({"chara_row_col_hira": chara_row_col_hira}),
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
  var hiragana = $(this).parents(".Table").data("hiragana");
  var chara_row_col_hira = [];
  sel.each(function () {
    chara_row_col_hira.push([$(this).data("character"), [$(this).data("row"), $(this).data("col"), hiragana]]);
  });
  console.log(chara_row_col_hira)
  $.ajax({
    url: $SCRIPT_ROOT + '/_ajax_state',
    type: "POST",
    data: JSON.stringify({"chara_row_col_hira": chara_row_col_hira}),
    contentType: "application/json; charset=utf-8",
  });
});

$(".sel-but[data-col='-1'][data-row='-1']").hover(function() {
  $(this).parents(".Table").find(".kana").not(".disable").toggleClass("hover");
});

$(".sel-but[data-col='-1'][data-row='-1']").dblclick(function() {
  $(this).parents(".Table").find(".kana").not(".disable").addClass("selected");
  var character = $(this).data("character").split(",");
  var hiragana = $(this).parents(".Table").data("hiragana");
  var chara_row_col_hira = [null, character, hiragana]
  $.ajax({
    url: $SCRIPT_ROOT + '/_ajax_state',
    type: "POST",
    data: JSON.stringify({"chara_row_col_hira": chara_row_col_hira}),
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
