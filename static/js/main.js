$(document).ready(function(){


    //Utility function: delays execution of the function func until doneTypingInterval ms after the last triggering event
  var typingTimer;
  var doneTypingInterval = 300;
  function delayExecute(func){
    clearTimeout(typingTimer);
    typingTimer = setTimeout(func,doneTypingInterval);
    return true;
  }

 $.template("search-doc-resultTemplate",
         "<a href='${FileURL}'>  ${SerialNumber} &nbsp; ${Title}  </a>"
 );

    
 $('#q').bind('keypress', function(event){

    delayExecute(ajaxSearch);
    //
    function ajaxSearch(){

        var query = $("#q").val();
        if(query !== ""){
            $.ajax({
                url:"search",
                data:{'q':query},
                success: function(data){
                    $("#search-doc-result").empty();
                    if(data.length == 0){
                        $("#search-doc-result").append(gettext("No Result"));
                    }
                    else{
                        for(item in data ){
                            $.tmpl( "search-doc-resultTemplate", data[item]).appendTo( "#search-doc-result" );
                        }
                    }
                }
            });

        }
        else{

            $("#search-doc-result").empty();
        }
    }

 });



});
