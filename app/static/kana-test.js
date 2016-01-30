$.fn.serializeObject = function()
{
   var o = {};
   var a = this.serializeArray();
   $.each(a, function() {
       if (o[this.name]) {
           if (!o[this.name].push) {
               o[this.name] = [o[this.name]];
           }
           o[this.name].push(this.value || '');
       } else {
           o[this.name] = this.value || '';
       }
   });
   return o;
};


$(document).keyup( function() {
    if(event.keyCode == 32) {
    if ($("#kanamoji").prop("disabled")) {
        $("#kanamoji").prop("disabled", false);
        $("#kanamoji").attr("placeholder", "Input the Romaji");
        $("#kanamoji").focus();
        $.ajax({
            url: $SCRIPT_ROOT + '/_ajax_test',
            type: "POST",
            data: JSON.stringify({"kanamoji": "start"}),
            contentType: "application/json; charset=utf-8",
            success: function(data) {
                $(".prev-kana span").text(data.display_kana[0]);
                $(".cur-kana span").text(data.display_kana[1]);
                $(".next-kana span").text(data.display_kana[2]);
                var d = new Date();
                d_time = d.getTime();
                $("#render_time").val(d_time);

            },
        });
    }
    }
});

var result = null;
var round_score = 0;
$("#kanamoji").keyup( function(event) {
  if(event.keyCode == 13) {
    var patt = new RegExp("[^A-z]");
    var kana_text = $("#kanamoji").val();
    if(kana_text.length < 4 && kana_text.length > 0 && !(patt.test(kana_text))) {
        var d = new Date();
        d_time = d.getTime();
        $("#submit_time").val(d_time);
        $.ajax({
            url: $SCRIPT_ROOT + '/_ajax_test',
            type: "POST",
            data: JSON.stringify($("#kana-form").serializeObject()),
            contentType: "application/json; charset=utf-8",
            success: function(data) {
                $(".prev-kana span").text(data.display_kana[0]);
                $(".cur-kana span").text(data.display_kana[1]);
                $(".next-kana span").text(data.display_kana[2]);
                $("#score").text(data.result[0]);
                if (data.result[1] == true) {
                    $("#cp").parents(".panel-header").addClass("right");
                    $("#cp").parents(".panel-header").removeClass("wrong");
                    $("#cp").text(data.result[2]);
                    $("#prev_right").text(data.romaji);
                    $("#prev_wrong").text("");
                } else {
                    $("#cp").parents(".panel-header").addClass("wrong");
                    $("#cp").parents(".panel-header").removeClass("right");
                    $("#cp").text(data.result[2]);
                    $("#prev_right").text(data.romaji);
                    $("#prev_wrong").text(kana_text);
                };
                $("#round_score").text(data.result[3])
                $("#next_kana_count").text(data.next_kana_count)
                var d = new Date();
                d_time = d.getTime();
                $("#render_time").val(d_time);
                $("#kanamoji").val("");
            },
        });


  } else {
//    $("#kanamoji").val("Please input 1 to 3 Letter");
  }}
});

$(".tabHead").children("div").click(function () {
    $(this).addClass("active");
    $(this).siblings().removeClass("active");
    var tabName = $(this).data("name");
    var content = $(this).parents(".Tabs").find(".tabContent").children()
    content.each(function () {
        if ($(this).data("name") == tabName) {
            $(this).addClass("active");
        } else {
            $(this).removeClass("active");
        }
    })
})

