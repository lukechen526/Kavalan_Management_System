$(document).ready(function(){

/* section for doc_engine */

//Utility function: delays execution of the function func until doneTypingInterval ms after the last triggering event
var typingTimer;
var doneTypingInterval = 700;
function delayExecute(func){
    clearTimeout(typingTimer);
    typingTimer = setTimeout(func,doneTypingInterval);
    return true;
}
$('#search-tabs select').chosen();
/*Document search*/
var current_page = 1;
    
function ajaxDocumentSearch(){

    var qw = $('#qw').val();
    var document_level  = $('#document_level').val();
    var tags = $('#tags').val();

    if(qw !== "" || tags != null || document_level != ""){

        $.ajax({
            url:"/doc_engine/api/documents",
            data:{query: JSON.stringify({qw: qw,
                                         document_level: document_level,
                                         tags: tags}),
                  page_number: current_page
            },
            error: function(jqXHR){$("#search-result").empty();},
            success: function(resp){
                $("#search-result").empty();
                var objects = resp['objects'];
                var page_number = resp['page_number'];
                current_page = page_number;
                var num_pages = resp['num_pages'];


                if(objects.length == 0){
                    $("#search-result").append(gettext("No Result"));
                }
                else{
                    objects.forEach(function(item){
                        $(_.template($('#search-doc-template').html(),item)).appendTo( "#search-result" );
                    });
                    //Enable Bootstrap popover for dekstop browser

                    if (!DetectIDevice()) {
                        $('.doc-link').popover();
                    }

                    if( num_pages > 1)
                    {
                        $(_.template($('#search-result-pagination-template').html(), {page_number:page_number, num_pages:num_pages})).appendTo("#search-result");

                        $('a.page').bind('click', function(event){
                            event.preventDefault();
                            current_page = parseInt($(event.target).attr('rel'));
                            delayExecute(ajaxDocumentSearch);
                         });
                    }
                }
            }
        });

    }
    
    else{

        $("#search-result").empty();
    }
}

var search_doc = function(event){
    current_page = 1;
    delayExecute(ajaxDocumentSearch);}
$('#qw, #tags').bind('keyup change', search_doc );
$('#document_level').chosen().change(search_doc);
$('#qw').autocomplete({
    source: '/doc_engine/autocomplete/',
    autoFocus: true
});





    
/* Batch Record Search*/
 function ajaxBatchRecordSearch(){
     $.ajax({
         url:"/doc_engine/api/batchrecords",
         data: {query:JSON.stringify({name: $("#name").val(),
                                      batch_number: $("#batch_number").val(),
                                      date_of_manufacture_from: $("#date_of_manufacture_from").val(),
                                      date_of_manufacture_to: $("#date_of_manufacture_to").val()}),
             
                page_number:current_page
         },
         error: function(jqXHR){$("#search-result").empty();},
         success: function(resp){
             $("#search-result").empty();
             var objects = resp['objects'];
             var page_number = resp['page_number'];
             var num_pages = resp['num_pages'];
             
             if(objects.length == 0){
                 $("#search-result").append(gettext("No Result"));
             }

             else{
                 objects.forEach(function(item){
                     $( _.template($('#search-batch-record-template').html(),item)).appendTo( "#search-result" );
                 });

                 if( num_pages > 1){
                     $(_.template($('#search-result-pagination-template').html(), {page_number:page_number, num_pages:num_pages})).appendTo("#search-result");
                     $('a.page').bind('click', function(event){
                         event.preventDefault();
                         current_page = parseInt($(event.target).attr('rel'));
                         delayExecute(ajaxBatchRecordSearch);
     });
                    }

             }

         }

     });


 }

$("#name, #batch_number, #date_manufactured_from, #date_manufactured_to")
    .bind("change keyup",function(event){
        current_page = 1;
        delayExecute(ajaxBatchRecordSearch)});
        
 (function(){
  //Override the default datepicker to display 民國
    $.datepicker.regional['zh-TW'] = {
        closeText: '關閉',
        prevText: '<上月',
        nextText: '下月>',
        currentText: '今天',
        monthNames: ['一月','二月','三月','四月','五月','六月',
        '七月','八月','九月','十月','十一月','十二月'],
        monthNamesShort: ['一月','二月','三月','四月','五月','六月',
        '七月','八月','九月','十月','十一月','十二月'],
        dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],
        dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],
        dayNamesMin: ['日','一','二','三','四','五','六'],
        dateFormat: 'yy-mm-dd', firstDay: 1,
        showMonthAfterYear: true,
        changeMonth: true,
        changeYear: true,
        isRTL: false,
        hideIfNoPrevNext: true,
        yearRange:'-15:+5'
    };
    $.datepicker.setDefaults($.datepicker.regional['zh-TW']);
    $.datepicker._phoenixGenerateMonthYearHeader = $.datepicker._generateMonthYearHeader;

    $.datepicker._generateMonthYearHeader = function(inst, drawMonth, drawYear, minDate, maxDate,
        secondary, monthNames, monthNamesShort) {
        
        var result = $($.datepicker._phoenixGenerateMonthYearHeader(inst, drawMonth, drawYear, minDate, maxDate,
            secondary, monthNames, monthNamesShort));
        result.children("select.ui-datepicker-year").children().each(function() {
            $(this).text('民國' + ($(this).text() - 1911) + '年');
        });

        if( inst.yearshtml ){
            var origyearshtml = inst.yearshtml;
            setTimeout(function(){
                //assure that inst.yearshtml didn't change.
                if( origyearshtml === inst.yearshtml ){
                    inst.dpDiv.find('select.ui-datepicker-year:first').replaceWith(inst.yearshtml);
                    inst.dpDiv.find('select.ui-datepicker-year').children().each(function() {
                        $(this).text('民國' + ($(this).text() - 1911) + '年');
                    });
                }
                origyearshtml = inst.yearshtml = null;
            }, 0);
        }
        return result.html();
    };


 })();


        var dates = $('#date_of_manufacture_from, #date_of_manufacture_to').datepicker({
            //Restrict the range of date for date_manufactured_to to those no earlier than date_manufactured_from
            onSelect:function (selectedDate) {
                var option = this.id == "date_of_manufacture_from" ? "minDate" : "maxDate",
                    instance = $(this).data("datepicker"),
                    date = $.datepicker.parseDate(
                        instance.settings.dateFormat ||
                            $.datepicker._defaults.dateFormat,
                        selectedDate, instance.settings);
                dates.not(this).datepicker("option", option, date);
            },
            onClose:function () {
                delayExecute(ajaxBatchRecordSearch);
            }

        });


//    Otherwise, change to input type to 'date' for mobile browsers
//    else {
//
//        $('#date_of_manufacture_from').get(0).type = 'date';
//        $('#date_of_manufacture_to').get(0).type = 'date';
//    }



/* Datepicker for adding Batch Records in Admin*/
$('#id_date_of_manufacture').datepicker();



/*Doc Engine tabs*/
var $tabs = $('#search-tabs').tabs();
$tabs.bind('tabsselect', function(event, ui){
     $('#search-result').empty();
     $(':input','#search-tabs form').not(':button, :submit, :reset, :hidden').val('').removeAttr('checked').removeAttr('selected');
     $('#search-tabs form *').find(".search-choice-close").trigger('click');

 });



});

