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


$(document).bind("keyup", "space", function() {
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
});

$("#kanamoji").keyup( function(event) {
  if(event.keyCode == 13) {
    if($("#kanamoji").val().length < 4 && $("#kanamoji").val().length > 0) {
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
                var d = new Date();
                d_time = d.getTime();
                $("#render_time").val(d_time);
                $("#kanamoji").val("");
            },
        });


  }}
});