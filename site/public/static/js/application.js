$(document).ready(function() {

    var aboutHash = window.location.hash;

    $("#showabout").on( "click", function () {
        if ($(window).scrollTop() >= 10) {
            $('body,html').animate({
                scrollTop: 0
            }, 500);
        }
        $(".aboutsection").css( "opacity","1" );
        $("#blogtitle").css( "opacity","0" );
        $("#descriptionheader").css( "opacity","0" );
     });
 
 
     $(".showblog").on( "click", function () {
        $(".aboutsection").css( "opacity","0" );
        $("#blogtitle").css( "opacity","1" );
        $("#descriptionheader").css(  "opacity","1" );
     });


    $('.photo-slideshow').pxuPhotoset({
                'rounded'   : 'false', // corners, all or false
                 'exif'      : true
            }, function() {
                // callback
    });

     
    if (aboutHash === "#about") {
        $("#showabout").trigger('click');
    }
 
 
});
    
$(window).on('scroll', function() {
    if ($(this).scrollTop() > 450)
        return false;
    //if ($(this).scrollTop() > 57) $('h2').css('position', 'fixed');
    $('.thelargeheader').css({
        'opacity':  1-(($(this).scrollTop())/400),
        'top': -($(this).scrollTop()/3)
    });
});
