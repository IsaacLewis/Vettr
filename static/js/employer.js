$(function(){
    $.get("http://localhost:8080/api/bookings?skype=robertwhitehead.07", function(data) {

   for( i in data) {
	var template = $("#skypeCall").html();
	var html = Mustache.to_html(template, data[i]);
	$('#place').append(html);	    
	}
	//$('#tag').attr("src", "http://google.com");

	$(".con").click(function() {
	alert("lads");
	    $("#" + $(this).attr("skype")).html("");
	alert($(this).attr("skype") + " " + $(this).attr("action") + globalskype);
	    $.get("/api/prospects/contact", function(data) {
	    });
	});
    });
});