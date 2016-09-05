
function show_followers(username, password, sourceId, destId, loadingId) {
	$(destId).hide();
    $(loadingId).show();
	auth = 'Basic ' + btoa(username+':' + password);
	url = '/api/showfollowers/' + username
    $.get(url, function(){
    }).done(function(showfollowers) {
        $(destId).text(showfollowers['followers'])
        $(loadingId).hide();
        $(destId).show();
    }).fail(function() {
        $(destId).text("{{ _('Error: Could not contact server.') }}");
        $(loadingId).hide();
        $(destId).show();
    });
}

function rate_book(bookid, rating) {
	rateurl = '/api/ratebook'
	$.ajax({
    	url: rateurl,
    	dataType: 'json',
    	type: 'post',
    	contentType: 'application/json',
    	data: JSON.stringify({ "bookid":bookid, "rating":rating}),
    	success: function( data, textStatus, jQxhr ){
			alert("Rating success")
    	},
    	error: function( jqXhr, textStatus, errorThrown ){
			alert("Rating error")
    	}
	});
}

$('.rateit').bind('rated reset', function (e) {
		alert("In bind")
         var ri = $(this);
 
         //if the use pressed reset, it will get value: 0 (to be compatible with the HTML range control), we could check if e.type == 'reset', and then set the value to  null .
         var value = ri.rateit('value');
         var productID = ri.data('productid'); // if the product id was in some hidden field: ri.closest('li').find('input[name="productid"]').val()
		alert(productID)
 
         //maybe we want to disable voting?
         ri.rateit('readonly', true);
 
         $.ajax({
             url: 'rateit.aspx', //your server side script
             data: { id: productID, value: value }, //our data
             type: 'POST',
             success: function (data) {
                 $('#response').append('<li>' + data + '</li>');
 
             },
             error: function (jxhr, msg, err) {
                 $('#response').append('<li style="color:red">' + msg + '</li>');
             }
         });
});

