$(".kana").not(".disable").click(function() {
  $(this).toggleClass("selected");
  var kanamoji = [$(this).children(".kanamoji").text()];
  console.log(kanamoji);
  $.ajax({
    url: $SCRIPT_ROOT + '/_ajax_state',
    type: "POST",
    data: JSON.stringify({
      "kanamoji": kanamoji
    }),
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
  var character = $(this).data("character");
  if (row === -1 && col === -1) {
    var sel = $(this).parents(".Table").find(".kana").not(".disable");
    sel.toggleClass("selected");
    var kanamoji = [];
    sel.each(function() {
      kanamoji.push($(this).children(".kanamoji").text());
    });
    $.ajax({
      url: $SCRIPT_ROOT + '/_ajax_state',
      type: "POST",
      data: JSON.stringify({
        "kanamoji": kanamoji
      }),
      contentType: "application/json; charset=utf-8",
    });
  }
  else if (row === -1) {
    var sel = $(this).parents(".Table").find(".kana[data-col='" + col + "'][data-row!='-1']").not(".disable");
    sel.toggleClass("selected");
    var kanamoji = [];
    sel.each(function() {
      kanamoji.push($(this).children(".kanamoji").text());
    });
    $.ajax({
      url: $SCRIPT_ROOT + '/_ajax_state',
      type: "POST",
      data: JSON.stringify({
        "kanamoji": kanamoji
      }),
      contentType: "application/json; charset=utf-8",
    });
  }
  else if (col === -1) {
    var sel = $(this).parents(".Table").find(".kana[data-col!='-1'][data-row='" + row + "'][data-character='" + character + "']").not(".disable");
    sel.toggleClass("selected");
    var kanamoji = [];
    sel.each(function() {
      kanamoji.push($(this).children(".kanamoji").text());
    });
    $.ajax({
      url: $SCRIPT_ROOT + '/_ajax_state',
      type: "POST",
      data: JSON.stringify({
        "kanamoji": kanamoji
      }),
      contentType: "application/json; charset=utf-8",
    });
  };
});

$(".sel-but").hover(function() {
  var i = $(this).data("col");
  var j = $(this).data("row");
  var character = $(this).data("character")
  if (j === -1) {
    $(this).parents(".Table").find(".kana[data-col='" + i + "'][data-row!='-1']").not(".disable").toggleClass("hover");
  };
  if (i === -1) {
    $(this).parents(".Table").find(".kana[data-col!='-1'][data-row='" + j + "'][data-character='" + character + "']").not(".disable").toggleClass("hover");
  };
});



$(".sel-but[data-col='-1'][data-row='-1']").hover(function () {
    $(this).parents(".Table").find(".kana").not(".disable").toggleClass("hover");
});

$(".sel-all").hover(
    function() {
        $(this).removeClass("hidden");
    }
);

$(".sel-all").click(function() {
  $(this).parents(".Table").find(".kana").not(".disable").addClass("selected");
  var sel = $(this).parents(".Table").find(".kana").not(".disable");
  var kanamoji = [null];
  sel.each(function () {
    kanamoji.push($(this).children(".kanamoji").text());
  });
  $.ajax({
    url: $SCRIPT_ROOT + '/_ajax_state',
    type: "POST",
    data: JSON.stringify({"kanamoji": kanamoji}),
    contentType: "application/json; charset=utf-8",
  });
});

$("form").submit(function(e) {
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