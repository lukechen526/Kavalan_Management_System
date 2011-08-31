$(document).ready(function(){

    //Event Handler for each Notification
    $('.notice-mark-seen').bind('click', function(e){
        e.preventDefault();
        var pattern = /notification\-(\d+)/;
        el = e.target;
        id = el.id.match(pattern)[1];
        $.ajax('/notification/'+id, {
            success: function(){
                //Remove the DOM element of the marked notification

                var options = {};
                notification_id = '#notification-' + id;
                nav_notification_id = '#nav-notification-' + id;
                $(notification_id).parents('li').toggle('puff', options, 'slow',function(){$(this).remove();});
                $(nav_notification_id).remove();

                //Change the unseen count at the navigation bar
                unseen_notices_count = parseInt($('#unseen-notices-count span').html());
                unseen_notices_count -=1;
                $('#unseen-notices-count span').html(unseen_notices_count+'');
                
                if(unseen_notices_count == 0){
                    $('#unseen-notices-count').removeClass('unseen');
                }


            }
        });

    });




    













});