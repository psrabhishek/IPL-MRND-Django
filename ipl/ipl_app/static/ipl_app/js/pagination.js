$(document).ready(function(){
    $('#data').after('<div id="nav"></div>');
    var rowsShown = 8;
    var rowsTotal = $('#data tbody tr').length;
    var numPages = rowsTotal/rowsShown;
    for(i = 0;i < numPages;i++) {
        var pageNum = i + 1;
        $('#nav').append('<a href="#" rel="'+i+'">'+pageNum+'</a> ');
    }
    $('#data tbody tr').hide();
    $('#data tbody tr').slice(0, rowsShown+1).show();
    $('#nav a:first').addClass('active');
    $('#nav a').bind('click', function(){

        $('#nav a').removeClass('active');
        $(this).addClass('active');
        var currPage = $(this).attr('rel');
        var startItem = currPage * rowsShown;
        var endItem = startItem + rowsShown;
        $('#data tbody tr').css('opacity','0.0').hide().slice(startItem, endItem).
        css('display','table-row').animate({opacity:1}, 300);
        $('#data tbody tr').css('opacity','0.0').slice(0, 1).
        css('display','table-row').animate({opacity:1}, 300);
    });

//    tabing - level 3 requirement
//    $('#tabs li').on('click', function() {
//    var tab = $(this).data('tab');
//
//    $('#tabs li').removeClass('is-active');
//    $(this).addClass('is-active');
//
//    $('#tab-content p').removeClass('is-active');
//    $('p[data-content="' + tab + '"]').addClass('is-active');
//  });
});