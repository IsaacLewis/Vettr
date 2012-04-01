$(function(){
    $.get("api/bookings?skype=" + globalSkype, function(data) {

alert("hello world");
   for( i in data) {
       
       data[i].when = new Date (data[i].when);
       data[i].when = data[i].when.toTimeString();
       var template = $("#skypeCall").html();
	
       var html = Mustache.to_html(template, data[i]);
	$('#place').append(html);	    
	}
	//$('#tag').attr("src", "http://google.com");

	$(".con").click(function() {
	    alert("ALDS");
	    //$("#" + $(this).attr("skype")).html("");
	    alert("/api/prospects/contact?prospectSkype=" + globalSkype + "&employerSkype=" + $(this).attr("skype"));
	    $.get("/api/prospects/contact?prospectSkype=" + globalSkype + "&employerSkype=" + $(this).attr("skype"), function(data) {
		alert("");
	    });
	});
    });
});