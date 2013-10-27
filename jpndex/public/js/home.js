var visible  = [0, 1, 2, 3, 4];
var _COLORS_ = ['#3ea4bf','#F6BB33', '#49bf92', '#a084bf', '#FF6A13'];
var colors   = ['#3ea4bf','#F6BB33', '#49bf92', '#a084bf', '#FF6A13'];

var margin = {top: 30, right: 20, bottom: 50, left: 50},
    width  = 760 - margin.left - margin.right,
    height = 400 - margin.top  - margin.bottom;

if( !window.isLoaded )
	window.addEventListener("load", function(){ onDocumentReady(); }, false);
else
	onDocumentReady();
	
function onDocumentReady(){
    var offset   = Date.today().getUTCOffset();
    var hour_ago = Date.parse(end).addHours(-1).toString('yyyy-MM-dd HH:mm:ss');
    //var end_hour = Date.parse(end).addHours(0).toString('yyyy-MM-dd HH:mm:ss');
    //var start_hour = Date.parse(start).addHours(0).toString('yyyy-MM-dd HH:mm:ss');
    var two_days = "start=" + start + "&end=" + end;
    var one_hour = "start=" + hour_ago + "&end=" + end;
    draw_dex(one_hour, two_days);
}

function draw_dex(one_hour, two_days){    
    
    var times = [];
    var ex = "key !== 'time'";

    var minDate = Date.parse(start);
    var maxDate = Date.parse(end);
    
    var x = d3.time.scale().domain([minDate, maxDate])
        .range([0, width]);
    
    var y = d3.scale.linear()
        .range([height, 0]);
        
    colors = []
    for(i in visible)
        colors.push(_COLORS_[visible[i]]);
        
    var color = d3.scale.ordinal().range(colors);
    
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom").ticks(12);
    
    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");
    
    var line = d3.svg.line()
        .interpolate("monotone")
        .x(function(d) { return x(d.time); })
        .y(function(d) { return y(d.score); });
    
    if($('#dex-graph').length)
        $('#dex-graph').remove()
        
    var svg = d3.select("#graph").insert("svg","#events")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("id", "dex-graph")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        
    var tooltip = d3.select("#graph")
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .attr("class", "tooltip-1");

    function make_x_axis() {        
        return d3.svg.axis()
            .scale(x)
             .orient("bottom")
             .ticks(48)
             /* .ticks(8) */
    }
    
    function make_y_axis() {        
        return d3.svg.axis()
            .scale(y)
            .orient("left")
            .ticks(10)
    }
 
    
    d3.json("../data/graph?"+two_days, function(error, data) {
        
        /*if(exclude != null) for(n in exclude) ex += " && key != '" + exclude[n] + "'";*/
                 
        color.domain(d3.keys(data[0]).filter(function(key) { return eval(ex); }));
        
        var table = [];
        var scores = [];
        var c = 0;        
        
        data.forEach(function(d) {
    	    times.push(d.time);
    	    table[c] = d['jpndex'];
    	    c ++;
        });
        
        var plots = color.domain().map(function(name){
          return{
              name: name,
              values: data.map(function(d){
                  scores.push(d[name]);
    		      return {time: Date.parse(d.time), score: d[name]};
              })
          };
        });
        
        x.domain([
            d3.min(plots, function(c) { return d3.min(c.values, function(v) { return v.time; }); }),
            d3.max(plots, function(c) { return d3.max(c.values, function(v) { return v.time; }); })
        ]);

        y.domain([
            d3.min(plots, function(c) { return d3.min(c.values, function(v) { return v.score; }); })*0.90,
            d3.max(plots, function(c) { return d3.max(c.values, function(v) { return v.score; }); })*1.1
        ]);

        svg.append("g")
          .attr("class", "x axis")
          .attr("id", "x-axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis)
          .style("opacity", "0")
          .transition().duration(50).delay(0).ease('in')
          .style("opacity", "1");
        
        d3.select("#x-axis")
          .append("text")
          .attr("class", "text")
          .attr("y", 32)
          .attr("x", 660)
          .attr("dy", ".71em")
          .text("Timeline")
          .style("opacity", "0")
          .transition().duration(50).delay(0).ease('in')
          .style("opacity", "1");
        
        svg.append("g")
          .attr("class", "y axis")
          .attr("id", "y-axis")
          .call(yAxis)
          .style("opacity", "0")
          .transition().duration(50).delay(0).ease('in')
          .style("opacity", "1");
        
        d3.select("#y-axis")    
          .append("text")
          .attr("class", "text")
          .attr("y", -5)
          .attr("x", 5)
          .attr("dy", ".71em")
          .text("Activity")
          .style("opacity", "0")
          .transition().duration(50).delay(0).ease('in')
          .style("opacity", "1");

        svg.append("g")         
        .attr("class", "grid")
        .attr("transform", "translate(0," + height + ")")
        .call(make_x_axis()
            .tickSize(-height, 0, 0)
            .tickFormat("")
        )

        svg.append("g")         
        .attr("class", "grid")
        .call(make_y_axis()
            .tickSize(-width, 0, 0)
            .tickFormat("")
        ) 
        
        var plot = svg.selectAll(".plot")
          .data(plots)
          .enter().append("g")
          .attr("class", "plot");
        
        plot.append("path")
          .style("stroke", "#fff")
          .style("opacity", "0")
          .transition().duration(500).delay(50).ease('in')
          .style("opacity", "1")
          .style("stroke", function(d) {return color(d.name); })
          .attr("d", function(d) {return line(d.values); })
          .attr("class",function(d) { return "line line-" + d.name.replace(/_/g,"-"); })    
    
    var indicator = svg.append("line")
    .attr("x1", 0)
    .attr("y1", height+10)
    .attr("x2", 0)
    .attr("y2", height-10)
    .style("stroke", "#3ea4bf")
    .style("stroke-width", "1.2px")
    .style("visibility", "hidden");
    
    var circle = svg.append("circle")
    .attr("r", 6)
    .attr("display", "none")
    .attr("class","tracker");

    d3.select('#dex-graph')
    .on("mouseover", function(){
        circle.attr("display", "block"); 
        tooltip.style("visibility", "visible");
        indicator.style("visibility", "visible");})
    .on("mousemove", update_circle)
    .on("mouseout", function(){ 
        circle.attr("display", "none"); 
        tooltip.style("visibility", "hidden"); 
        indicator.style("visibility", "hidden");});
    
        
    var max_score = d3.max(scores)*1.1;
    var min_score = d3.min(scores)*0.9;
    
    var spacing = 4800;
    
    function update_circle(){
        var xpos  = d3.mouse(this)[0] - margin.left;
        var index = Math.round((table.length-1)*(xpos/width));
        var ypos;
        
        console.log(index)
        
        if(xpos > 0 && xpos < width){
            /*
            if( table[index] === undefined ){     
                var lower = Math.floor(index);
                var upper = Math.floor(index) + 1;
    
                var between = d3.interpolateNumber(
                    (height - ((table[lower] - min_score) / ((max_score- min_score) / height))), 
                    (height - ((table[upper] - min_score) / ((max_score- min_score) / height))));
                ypos = between( (xpos % spacing) / spacing );
                
            } 
            */
            //else{
                ypos = height - ((table[index]-min_score) / ((max_score-min_score)/height));
            //}
            circle
            .attr("cx", xpos)
            .attr("cy", ypos);
            
            indicator
            .attr("x1", xpos)
            .attr("x2", xpos)
            .attr("y1", 0)
            .attr("y2", height+10);
            
            tooltip.style("visibility", "visible")
            tooltip.style("top", (ypos+80)+"px").style("left",(d3.event.pageX+20)+"px")
            
            var time = times[Math.floor(index)];
            var h  = Date.parse(time).addHours(1).toString('yyyy-MM-dd HH:mm'); //Gotcha UTC!!
            var h1 = "start=" + time + "&end=" + h;
            var c = 0;
            var cap = 5;
            var display_date = Date.parse(time).toString('MMM d,  h:mmtt')
            var word = "<h4>"+display_date+"</h4><ul>"
            
            d3.json("../data/cloud?"+h1, function(error, data) {
                data.forEach(function(d) {
                    if(c < cap)
                        word = word + "<li>" + d.term + '</li>';
                    c++;
                });
                $('.tooltip-1').html(word+'</ul>');
            });
        }
    }
    
    var key = svg.append("svg:g");
    key.append("svg:circle")
          .attr("cy", 355 )
          .attr("cx", 0 )
          .attr("r", 8) // radius of circle
          /* .attr("fill", '#ff8a2b') */
          .attr("fill", '#F6BB33')
          .attr("stroke", '#999999') 
          .style("opacity", 0.9);
    key.append("text")
            .attr("y", 350)
            .attr("x", 15)
            .attr("dy", ".71em")
            .attr("class", "text")      
            .text("Volume");
    key.append("svg:circle")
          .attr("cy", 355 )
          .attr("cx", 80 )
          .attr("r", 8) // radius of circle
          /* .attr("fill", '#ff8a2b') */
          .attr("fill", '#3ea4bf')
          .attr("stroke", '#999999') 
          .style("opacity", 0.9);
    key.append("text")
            .attr("y", 350)
            .attr("x", 95)
            .attr("dy", ".71em")
            .attr("class", "text")      
            .text("Sentiment");
    
    
    });
    
        
    d3.json("../home/map?"+one_hour, function(error, data) {
        data.forEach(function(d) {
    	    d3.select("#"+d.name).attr("r", d.size).style('opacity',1/(Math.log(d.size)))        
    	    .append("text")
            .attr("class", "text")
            .attr("y", -5)
            .attr("x", 5)
            .attr("dy", ".71em")
            .text(d.name)
            .style("opacity", "0")
            .transition().duration(50).delay(0).ease('in')
            .style("opacity", "1");
        });
    });
}


