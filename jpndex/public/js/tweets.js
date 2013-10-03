var tweets;
var from = 20;
var to   = 39;
var loading = true;

if( !window.isLoaded )
	window.addEventListener("load", function(){ onDocumentReady(); }, false);
else
	onDocumentReady();
	
function onDocumentReady(){    
    query = window.location.href.slice(window.location.href.indexOf('?') + 1)
    
    get_tweets(function(data){
        //do something with data responded from the server
        load_more(data);
        $(window).scroll(function() {
            if($(window).scrollTop() == $(document).height() - $(window).height()) {
                // ajax call get data from server and append to the div
                loading = true;
                load_more(data);
            }
            else{
                loading = false;
            }
        });
        
    });
}

$.fn.appendText = function(text) {
    this.each(function() {
        var textNode = document.createTextNode(text);
        $(this).append(textNode);
    });
};     
    
function load_more(tweets){        
    if( to < Object.keys(tweets).length ){
        for(var i=from;i<to;i++)
            append_tweet(tweets[i]);    
        from = to + 1;
        to += 20;
    }
}

function get_tweets(callback){
    var $ret = 0;    
    $('#loading').css('display', 'inline-block');
    fading();
    
    $.ajax({
        type: 'GET',
        url:  '../tweets/tweets?' + query,
        cache: false,
        success: function(data){ callback(data); }
    });
    return $ret;
}

function fading() {
    if(loading){
        $("#tweets-footer .webfont.icon").animate({opacity:'+=1'}, 1000);
        $("#tweets-footer .webfont.icon").animate({opacity:'-=0.7'}, 1000, fading);
        $('#loading').css('display', 'inline-block');
        $("#loading").animate({opacity:'+=1'}, 1000);
        $("#loading").animate({opacity:'-=0.7'}, 1000, fading);
    }
    else{
        $("#tweets-footer .webfont.icon").css('opacity', 1.0);
        $('#loading').css('display', 'none');    
    }
    
}

function append_tweet(tweet){
    $("#timeline").append('<li><a href=https://twitter.com/'+tweet.user+' class=profile target=_blank><img src='+tweet.avatar+' onError="this.onerror=null; this.src=\'../public/images/default_profile.png\'" /></a><div class=tweet><a href=https://twitter.com/'+tweet.user+' class=user-link target=_blank><h4>'+tweet.name+' <span class=username>@'+tweet.user+'</span></h4></a>'+tweet.tweet+'</div><div class=twitter-buttons><div class=timestamp>'+tweet.timestamp+'</div><a href=https://twitter.com/'+tweet.user+'/status/'+tweet.id+' style=margin-right:10px; target=_blank>view on twitter</a></div></li>')
}
