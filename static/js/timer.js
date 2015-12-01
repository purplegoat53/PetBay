function padNum(s, length) {
    if(s.length < length)
    	return "0".repeat(length - s.length) + s;
    return s;
}

setInterval(function() {
    $(".timer").each(function() {
        var time_left = parseInt($(this).data("time_left"));
        if(time_left < 0)
            $(this).parent(".thumbnail").parent(".thumb").remove();
        var hours = parseInt(time_left/3600) % 24;
        var minutes = parseInt(time_left/60) % 60;
        var seconds = parseInt(time_left) % 60;
        var timer_str = padNum(hours.toString(), 2) + ":" + padNum(minutes.toString(), 2) + ":" + padNum(seconds.toString(), 2);
        $(this).data("time_left", time_left-1);
        $(this).text(timer_str);
    });
}, 1000);
