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
         $('.active').not('#account-menu, #account-menu *').removeClass('active');
         $('#account-menu, #account-menu *').toggleClass('active');
    });

    $("#unseen-notices-count").bind('click', function(event){
            event.preventDefault();
            $('.active').not('#notices, #notices * ').removeClass('active');
            $('#notices, #notices *').toggleClass('active');
    });

    $("#options-icon").bind('click', function(event){
            event.preventDefault();
            $('.active').not('#options, #options *').removeClass('active');
            $('#options, #options *').toggleClass('active');
    });

});
