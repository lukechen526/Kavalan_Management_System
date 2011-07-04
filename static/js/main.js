$(document).ready(function(){


    //Utility function: delays execution of the function func until doneTypingInterval ms after the last triggering event
  var typingTimer;
  var doneTypingInterval = 700;
  function delayExecute(func){
    clearTimeout(typingTimer);
    typingTimer = setTimeout(func,doneTypingInterval);
    return true;
  }

 $.template("search-doc-resultTemplate",
         "<a href='${file_url}'>  ${serial_number} &nbsp; ${title}  </a>"
 );

 $('#q').bind('keyup change', function(event){

    delayExecute(ajaxSearch);
    //
    function ajaxSearch(){

        var query = $("#q").val();
        if(query !== ""){
            $.ajax({
                url:"/api/documents/",
                data:{'q':query},
                success: function(data){
                    $("#search-doc-result").empty();
                    console.log(data);
                    if(data.length == 0){
                        $("#search-doc-result").append(gettext("No Result"));
                    }
                    else{
                        data.forEach(function(item){
                            $.tmpl( "search-doc-resultTemplate", item).appendTo( "#search-doc-result" );
                        });

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
