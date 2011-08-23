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
 $('#q, #document_level, #labels').bind('keyup change', function(event){

    delayExecute(ajaxDocumentSearch);
     
    function ajaxDocumentSearch(){

        var query = $('#q').val();
        var document_level  = $('#document_level').val();
        var labels = $('#labels').val();
        
        if(query !== ""){
            $.ajax({
                url:"/api/documents",
                data:{'q':query, 'document_level': document_level, 'labels':labels},
                success: function(data){
                    $("#search-result").empty();
                    if(data.length == 0){
                        $("#search-result").append(gettext("No Result"));
                    }
                    else{
                        data.forEach(function(item){
                            $(_.template($('#search-doc-template').html(),item)).appendTo( "#search-result" );
                        });

                    }
                }
            });

        }
        else{

            $("#search-result").empty();
        }
    }
 });

    
/* Batch Record Search*/

 function ajaxBatchRecordSearch(){
     $.ajax({
         url:"/api/batchrecords",
         data: {name: $("#name").val(),
               batch_number: $("#batch_number").val(),
               date_manufactured_from: $("#date_manufactured_from").val(),
               date_manufactured_to: $("#date_manufactured_to").val()},
         error: function(jqXHR){$("#search-result").empty();},
         success: function(data){
             $("#search-result").empty();
             if(data.length == 0){
                 $("#search-result").append(gettext("No Result"));
             }

             else{
                  data.forEach(function(item){
                      $( _.template($('#search-batch-record-template').html(),item)).appendTo( "#search-result" );
                   });

             }


         }




     });


 }
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

 var dates = $('#date_manufactured_from, #date_manufactured_to').datepicker({
     //Restrict the range of date for date_manufactured_to to those no earlier than date_manufactured_from
     onSelect: function( selectedDate ) {
             var option = this.id == "date_manufactured_from" ? "minDate" : "maxDate",
                 instance = $( this ).data( "datepicker" ),
                 date = $.datepicker.parseDate(
                     instance.settings.dateFormat ||
                     $.datepicker._defaults.dateFormat,
                     selectedDate, instance.settings );
             dates.not( this ).datepicker( "option", option, date );
         },
     onClose: function(){delayExecute(ajaxBatchRecordSearch);}

 });

$("#name").bind("change keyup",function(event){delayExecute(ajaxBatchRecordSearch)});
$("#batch_number").bind("change keyup",function(event){delayExecute(ajaxBatchRecordSearch)});
$("#date_manufactured_from").bind("change keyup",function(event){delayExecute(ajaxBatchRecordSearch)});
$("#date_manufactured_to").bind("change keyup",function(event){delayExecute(ajaxBatchRecordSearch)});


/*Doc Engine tabs*/
 $('#search-tabs').tabs();
 $('#search-tabs').bind('tabsselect', function(){
     $('#search-result').empty();
     $('#search-tabs form').each(function(){this.reset();});});

/* Datepicker for adding Batch Records in Admin*/
 $('#id_date_manufactured').datepicker();


});