$(function(){
    $.get("api/bookings?skype=" + globalSkype, function(data) {


   for( i in data) {
       
       //data[i].when = new Date (data[i].when);
       //data[i].when = data[i].when.toTimeString();
       var template = $("#skypeCall").html();
	
       var html = Mustache.to_html(template, data[i]);
	$('#place').append(html);	    
	}
	//$('#tag').attr("src", "http://google.com");

	$(".con").click(function() {
	    alert("Connection made, an email will be sent later this afternoon");
	    //$("#" + $(this).attr("skype")).html("");
//	    alert("/api/prospects/contact?prospectSkype=" + globalSkype + "&employerSkype=" + $(this).attr("skype"));
	    $.get("/api/prospects/contact?prospectSkype=" + globalSkype + "&employerSkype=" + $(this).attr("skype"), function(data) {
	    });
	});
    });
});