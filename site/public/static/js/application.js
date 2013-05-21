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
    // jQuery for the banner placement
    if ( $('#banner').length )
    {
        if ($(this).scrollTop() > 300)
            return false;
        if ($(this).scrollTop() > 254)
        {
            $('#banner').css({'background-color': '#ddd', 'position': 'fixed', 'top': 0, 'width': '100%', 'text-align': 'center'});
            $('h2 span').show();
            $('#content').css({'margin-top': '110px'});
        }
        else if($(this).scrollTop() < 254)
        {
            $('#banner').css({'background-color': 'transparent', 'position': 'static', 'top': 'auto', 'width': '100%', 'text-align': 'center'});
            $('h2 span').hide();
            $('#content').css('margin-top', 'auto');
        }
    }

    if ($(this).scrollTop() > 190)
        return false;
    $('.thelargeheader').css({
        'opacity':  1-(($(this).scrollTop())/300),
        'top': -($(this).scrollTop()/3)
    });
});
