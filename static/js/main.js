$(document).ready(function(){
 $('#q').bind('keyup', function(event){

     ajaxSearch();
    //
    function ajaxSearch(){

        var query = $("#q").val();
        console.log(query);
        $.ajax({
            url:"search",
            data:{'q':query},
            success: function(data){
                $("#result").empty();
                console.log("Received data:");
                console.log(data);
                console.log(data.length);
                if(data.length == 0){
                    $("#result").append(gettext("No Result"));
                }
                else{

                    $("#result").append(JSON.stringify(data));

                }
            }
        });
    }

 });

});
