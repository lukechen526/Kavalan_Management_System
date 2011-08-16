$(document).ready(function(){
    
     //Prevents the browser from caching the JSON response.
    $.ajaxSetup({ cache: false });

    /* Style buttons with jQuery UI*/
    $('input:submit, input:reset').button();

    /* section for navigation bar */

      //Mark the current link in the nav bar
     $("nav ul li a").each(function(){

        if($(this).attr("href") == window.location.pathname)
        {
            $(this).addClass("current");
        }
     });

    //Toggle the display of account-options based on clicking of #username

     $("#expand-menu").bind('click', function(event){
         event.preventDefault();
         $('#options-icon, #options-menu').removeClass('active');
         $('#expand-menu, #username, #account-options').toggleClass('active');
     });

     $("#options-icon").bind('click', function(event){
            event.preventDefault();
            $('#expand-menu, #username, #account-options').removeClass('active');
            $('#options-icon, #options-menu').toggleClass('active');
     });



    
});
