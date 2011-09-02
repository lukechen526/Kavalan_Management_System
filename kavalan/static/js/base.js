$(document).ready(function(){
    
     //Prevents the browser from caching the JSON response.
    $.ajaxSetup({ cache: false });

    /* section for navigation bar */

      //Mark the current link in the nav bar
    $("nav ul li a").each(function(){

       if($(this).attr("href") == window.location.pathname)
       {
         $(this).addClass("active");
       }
    });

    //Toggle the display of account-options based on clicking of #username

    $("#expand-menu").bind('click', function(event){
         event.preventDefault();
         $('.open').not('#account-menu, #account-menu *').removeClass('open');
         $('#account-menu, #account-menu *').toggleClass('open');
    });

    $("#unseen-notices-count").bind('click', function(event){
            event.preventDefault();
            $('.open').not('#notices, #notices * ').removeClass('open');
            $('#notices, #notices *').toggleClass('open');
    });

    $("#options-icon").bind('click', function(event){
            event.preventDefault();
            $('.open').not('#options, #options *').removeClass('open');
            $('#options, #options *').toggleClass('open');
    });

});
