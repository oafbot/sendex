var start;
var end;

function round_hour(d) {
    /*d.setMinutes (d.getMinutes() + 30);
    d.setMinutes (0);*/
    d.setHours(d.getHours() + Math.floor(d.getMinutes()/60));
    d.setMinutes(0);

    return d;
}