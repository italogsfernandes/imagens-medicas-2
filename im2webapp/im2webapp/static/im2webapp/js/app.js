function close_messages(){
    $("#messages .close").each(function(i){
        window.setTimeout(function(){
                $('#messages .close').first().alert('close');
            },
            (i + 1) * 10000
        );
    });
}

$(window).bind("load", function() {
    close_messages();
});
