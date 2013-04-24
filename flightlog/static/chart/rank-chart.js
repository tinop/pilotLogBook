// Dimensions.
const DIMENSIONS = getWindowDimensions();
const WIDTH = DIMENSIONS.width - 20;    // 20 => padding.
const HEIGHT = DIMENSIONS.height - 20;  // 50 => padding.

// Insets.
const INSETS = {'left': 150, 'right': 150, 'top': 30, 'bottom': 30};

// Padding.
const PADDING = {'left': 20, 'right': 20, 'top': 20, 'bottom': 20};

// Tick-mark length.
const TICK_MARK_LENGTH = 8;

// Marker radius.
const MARKER_RADIUS = 10;

// Scales.
const SCALES = {};

// Transition durations.
const TRANSITION_DURATION = 1000;
const QUICK_TRANSITION = 350;

// Opacity of dimmed and highlighted objects.
const DIMMED_OPACITY = 0.25;
const HIGHLIGHT_OPACITY = 1.0;

// Zoom factors.
const ZOOM_PEAK = 5.0;
const ZOOM_SHOULDER = 3.0;

// Zooming.
var zoomed = false;

// Visualize when document has loaded.
//
window.onload = function() {

    // Load data.
    d3.json("static/chart/ranks.json", function(data) {

        // Process lap markers..
        data.rankMarkers = processRankMarkers(data);
        data.offsetMarkers = processOffsets(data);

        // Visualize the data.
        visualize(data);
    });
};

function processRankMarkers(data) {

    var markers = [];
    var p = 0;
    for (var i = 0;
         i < data.rankings.length;
         i++) {

        var rankData = data.rankings[i];
        var ranks = rankData.ranks;
        if (ranks != undefined) {
            for (var j = 0;
                 j < ranks.length;
                 j++) {

                var rank = ranks[j];
                var marker = {};
                marker.start = rankData.ranks[0];
                marker.week = rankData.offset + j;
                marker.rank = rank;
                marker.name = rankData.name;

                markers[p++] = marker;
            }
        }
    }
    return markers;
}

function processOffsets(data) {

    var markers = [];
    var p = 0;
    for (var i = 0;
         i < data.rankings.length;
         i++) {

        var rankData = data.rankings[i];
        var offset = rankData.offset;
        if (offset != undefined && offset != 0) {

            var marker = {};
            marker.start = rankData.ranks[0];
            marker.week = offset;
            marker.rank = rankData.ranks[0];
            marker.name = rankData.name;

            markers[p++] = marker;
        }
    }
    return markers;
}

// Create the visualization.
//
// data the lap data object.
//
function visualize(data) {

    // Configure scales.
    configureScales(data);

    var vis = d3.select('#chart')
        .append('svg:svg')
        .attr('width', WIDTH)
        .attr('height', HEIGHT)
        .attr('class', 'zoom');

    // Background rect to catch zoom clicks.
    vis.append('svg:rect')
        .attr('class', 'zoom')
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', WIDTH)
        .attr('height', HEIGHT)
        .style('opacity', 0.0);

    // Week tick-lines.
    addWeekTickLines(vis, data.weeks.internal.length);

    // Week labels.
    addWeekLabels(vis, data.weeks.internal.length, data.weeks.labels, SCALES.y.range()[0] - PADDING.bottom, '0.0em', 'top');
    addWeekLabels(vis, data.weeks.internal.length, data.weeks.labels, SCALES.y.range()[1] + PADDING.top, '0.35em', 'bottom');

    // Add ranking poly-lines.
    addRankingLines(vis, data.rankings);

    // Add name labels.
    addPlayerLabels(vis, data.rankings, false, 'initNames', SCALES.x(0) - PADDING.right, 'end')
        .attr('y', function (d) {

            return SCALES.y(d.ranks[0] - 1);
        });
    addPlayerLabels(vis, data.rankings, true, 'curNames', SCALES.x(data.weeks.internal.length) + PADDING.left, 'start')
        .attr('y', function (d, i) {

            return SCALES.y(i);
        });

    // Add markers.
    addOffsetMarkers(vis, data.offsetMarkers, "offset");
    addRankMarkers(vis, data.rankMarkers, "rank");

    // Listen for clicks -> zoom.
//     vis.selectAll('.zoom')
//         .on("click", function() {
// 
//             toggleZoom(vis, d3.mouse(this)[0]);
//         });
}

// Configure the scales.
//
// data: data set.
//
function configureScales(data) {

    SCALES.x = d3.scale.linear()
        .domain([0, data.weeks.internal.length])
        .range([INSETS.left, WIDTH - INSETS.right]);

    SCALES.y = d3.scale.linear()
        .domain([0, data.rankings.length - 1])
        .range([INSETS.top, HEIGHT - INSETS.bottom]);

    SCALES.clr = d3.scale.category20();
}

// Highlight player.
//
// vis: the data visualization root.
// index: index of player to highlight.
//
function highlight(vis, name) {

    // Dim others.
    vis.selectAll('polyline')
        .transition()
        .duration(QUICK_TRANSITION)
        .style('opacity', function(d) {

            return d.name == name ? HIGHLIGHT_OPACITY : DIMMED_OPACITY;
        });

    vis.selectAll('circle.marker.offset')
        .transition()
        .duration(QUICK_TRANSITION)
        .style('opacity', function(d) {

            return d.name == name ? HIGHLIGHT_OPACITY : DIMMED_OPACITY;
        });

    vis.selectAll('circle.marker.rank')
        .transition()
        .duration(QUICK_TRANSITION)
        .style('opacity', function(d) {

            return d.name == name ? HIGHLIGHT_OPACITY : 0.0;
        });

    vis.selectAll('text.label.initNames')
        .transition()
        .duration(QUICK_TRANSITION)
        .style('opacity', function(d) {

            return d.name == name ? HIGHLIGHT_OPACITY : DIMMED_OPACITY;
        });

    vis.selectAll('text.label.curNames')
        .transition()
        .duration(QUICK_TRANSITION)
        .style('opacity', function(d) {

            return d.name == name ? HIGHLIGHT_OPACITY : DIMMED_OPACITY;
        });

    vis.selectAll('text.label.marker')
        .transition()
        .duration(QUICK_TRANSITION)
        .style('opacity', function(d) {

            return d.name == name ? HIGHLIGHT_OPACITY : 0.0;
        });
}

// Remove highlights.
//
// vis: the data visualization root.
//
function unhighlight(vis) {

    // Reset opacity.
    vis.selectAll('polyline')
        .transition()
        .duration(QUICK_TRANSITION)
        .style('opacity', HIGHLIGHT_OPACITY);
    vis.selectAll('circle.marker.offset')
        .transition()
        .duration(QUICK_TRANSITION)
        .style('opacity', HIGHLIGHT_OPACITY);
    vis.selectAll('circle.marker.rank')
        .transition()
        .duration(QUICK_TRANSITION)
        .style('opacity', 0.0);
    vis.selectAll('text.label.initNames')
        .transition()
        .duration(QUICK_TRANSITION)
        .style('opacity', HIGHLIGHT_OPACITY);
    vis.selectAll('text.label.curNames')
        .transition()
        .duration(QUICK_TRANSITION)
        .style('opacity', HIGHLIGHT_OPACITY);
    vis.selectAll('text.label.marker')
        .transition()
        .duration(QUICK_TRANSITION)
        .style('opacity', 0.0);
}

// Zoom/unzoom.
//
// vis: the data visualization root.
// mouseX: x-coordinate of mouse click.
//
function toggleZoom(vis, mouseX) {

    // Get week of mouse-click position.
    var week = Math.round(SCALES.x.invert(mouseX));

    // Clamp to domain.
    var domain = SCALES.x.domain();
    week = Math.max(domain[0], Math.min(domain[1], week));

    // Specify transform.
    var xform = zoomed ? unzoomXform : zoomXform;
    zoomed = !zoomed;

    // Transition tick lines.
    vis.selectAll('line.tickLine')
        .transition()
        .duration(TRANSITION_DURATION)
        .attr("x1", function(d) {

            return SCALES.x(xform(d + 0.5, week))
        })
        .attr("x2", function(d) {

            return SCALES.x(xform(d + 0.5, week))
        });

    // Transition tick labels.
    vis.selectAll('text.week')
        .transition()
        .duration(TRANSITION_DURATION)
        .attr("x", function(d) {

            return SCALES.x(xform(d, week))
        });

    // Transition lapped elements.
    vis.selectAll('polyline.ranking')
        .transition()
        .duration(TRANSITION_DURATION)
        .attr('points', function(d) {

            var points = [];

            if (d.offset == 0)
                points.push(SCALES.x(xform(0.0, week)) + ',' + SCALES.y(d.ranks[0] - 1));

            for (var i = 0;
                 i < d.ranks.length;
                 i++) {

                points.push(SCALES.x(xform(i+d.offset+0.5, week)) + ',' + SCALES.y(d.ranks[i] - 1));
            }

            if (points.length > 0)
                points.push(SCALES.x(xform(i + d.offset, week)) + ',' + SCALES.y(d.ranks[i - 1] - 1));

            return points.join(' ');
        });

    // Transition markers (circles).
    vis.selectAll('circle.marker')
        .transition()
        .duration(TRANSITION_DURATION)
        .attr('cx', function(d) {

            return SCALES.x(xform(d.week, week));
        });

    // Transition markers (labels).
    vis.selectAll('text.label.marker')
        .transition()
        .duration(TRANSITION_DURATION)
        .attr('x', function(d) {

            return SCALES.x(xform(d.week, week));
        });
}

/**
 * The zooming function is piecewise linear.  It divides the x-axis into several sections each of which is zoomed by
 * a different amount.  The closer the zone is to the zoom centre, the higher the zoom factor.
 *
 * | NO ZOOM | ZOOM_SHOULDER | ZOOM_PEAK | ZOOM_SHOULDER | NO ZOOM |
 *
 * ZOOM_PEAK is applied where on the lap where the user clicked.
 * ZOOM_SHOULDER is applied to the laps either side of this.
 * No zoom is applied elsewhere.
 *
 * @param x the x-coordinate to transform using the zooming function.
 * @param lap the lap the user clicked on.
 */
function zoomXform(x, lap) {

    // The x-axis domain.
    var domain = SCALES.x.domain();
    var step = domain[1] - domain[0];

    // What is the increment between each lap after zooming.
    var inc = lap <= domain[0] || lap >= domain[1] ?
        step / (ZOOM_PEAK + ZOOM_SHOULDER - 2.0 + step) :
        step / (ZOOM_PEAK + 2.0 * ZOOM_SHOULDER - 3.0 + step);

    // The zoom centre is mid-lap.
    lap += 0.5;

    // The transformed version of x.
    var z = 0.0;

    // Beyond upper shoulder.
    if (x > lap + 1.0) z = (x + ZOOM_PEAK + 2.0 * ZOOM_SHOULDER - 3.0) * inc;

    // Upper shoulder.
    else if (x > lap) z = ((x - lap + 1.0) * ZOOM_SHOULDER + lap + ZOOM_PEAK - 2.0) * inc;

    // Peak.
    else if (x > lap - 1.0) z = ((x - lap + 1.0) * ZOOM_PEAK + lap + ZOOM_SHOULDER - 2.0) * inc;

    // Lower shoulder.
    else if (x > lap - 2.0)   z = ((x - lap + 2.0) * ZOOM_SHOULDER + lap - 2.0) * inc;

    // Below lower shoulder.
    else z = (x - domain[0]) * inc;

    return z;
}

function unzoomXform(x) {

    return x;
}

// Add week tick-lines.
//
// vis: the data visualization root.
// numWeeks: number of weeks to be displayed
//
function addWeekTickLines(vis, numWeeks) {

    vis.selectAll('line.tickLine')
        .data(SCALES.x.ticks(numWeeks))
        .enter().append('svg:line')
        .attr('class', 'tickLine zoom')
        .attr('x1', function(d) {

            return SCALES.x(d);
        })
        .attr('x2', function(d) {

            return SCALES.x(d);
        })
        .attr('y1', SCALES.y.range()[0] - TICK_MARK_LENGTH)
        .attr('y2', SCALES.y.range()[1] + TICK_MARK_LENGTH)
        .attr('visibility', function(d) {

            return d <= numWeeks ? 'visible' : 'hidden'
        });
}

// Add week labels.
//
// vis: the data visualization root.
// numWeeks: number of weeks to be displayed
// labels: week labels
// y: y position of labels.
// dy: y offset.
// cssClass: CSS class id.
//
function addWeekLabels(vis, numWeeks, labels, y, dy, cssClass) {

    vis.selectAll('text.week.' + cssClass)
        .data(SCALES.x.ticks(numWeeks))
        .enter().append('svg:text')
        .attr('class', 'week ' + cssClass + ' zoom')
        .attr('x', function(d) {

            return SCALES.x(d - 0.5);
        })
        .attr('y', y)
        .attr('dy', dy)
        .attr('text-anchor', 'middle')
        .text(function(d, i) {

            return (i > 0 && i <= labels.length) ? labels[i-1] : '';
        });
}

// Add ranking polyline elements.
//
// vis: the visualization root.
// ranks: ranking data.
//
function addRankingLines(vis, rankings) {

    vis.selectAll('polyline.ranking')
        .data(rankings)
        .enter()
        .append('svg:polyline')
        .attr('class', 'ranking zoom')
        .attr('points', function(d) {

            var points = [];

            if (d.offset == 0)
                points.push(SCALES.x(0) + ',' + SCALES.y(d.ranks[0] - 1));

            for (var i = 0;
                 i < d.ranks.length;
                 i++) {

                points.push(SCALES.x(i+d.offset + 0.5) + ',' + SCALES.y(d.ranks[i] - 1));
            }

            if (points.length > 0)
                points.push(SCALES.x(i + d.offset) + ',' + SCALES.y(d.ranks[i - 1] - 1));

            return points.join(' ');
        })
        .style('stroke', function(d) {

            return SCALES.clr(d.ranks[0]);
        })
        .on('mouseover', function(d) {

            highlight(vis, d.name);
        })
        .on('mouseout', function() {

            unhighlight(vis);
        });
}

// Add player name labels.
//
// vis: the data visualization root.
// rankings: the data.
// showAllPlayers: do we drop offset != 0 players?
// cssClass: CSS class id.
// textAnchor: text-anchor value.
//
function addPlayerLabels(vis, rankings, showAllPlayers, cssClass, x, textAnchor) {

    return vis.selectAll('text.label.' + cssClass)
        .data(rankings)
        .enter()
        .append('svg:text')
        .attr('class', 'label ' + cssClass)
        .attr('x', x)
        .attr('dy', '0.35em')
        .attr('text-anchor', textAnchor)
        .text(function(d) {

            return (showAllPlayers || d.offset == 0) ? d.name : '';
        })
        .style('fill', function(d) {

            return SCALES.clr(d.ranks[0]);
        })
        .on('mouseover', function(d) {

            highlight(vis, d.name);
        })
        .on('mouseout', function() {

            unhighlight(vis);
        });
}

// Add rank markers.
//
// vis: the visualization root.
// data: marker data.
// class: marker sub-class.
//
function addRankMarkers(vis, data, cssClass) {

    // Place circle glyph.
    vis.selectAll("circle.marker." + cssClass)
        .data(data)
        .enter()
        .append("svg:circle")
        .attr("class", "marker " + cssClass + " zoom")
        .attr("cx", function(d) {

            return SCALES.x(d.week + 0.5);
        })
        .attr("cy", function(d) {

            return SCALES.y(d.rank - 1);
        })
        .attr("r", MARKER_RADIUS)
        .style("fill", function(d) {

            return SCALES.clr(d.start);
        })
        .style('opacity', 0.0)
        .on('mouseover', function(d) {

            highlight(vis, d.name);
        })
        .on('mouseout', function() {

            unhighlight(vis);
        });

    // Place text.
    vis.selectAll("text.label.marker." + cssClass)
        .data(data)
        .enter()
        .append("svg:text")
        .attr("class", "label marker " + cssClass + " zoom")
        .attr("x", function(d) {

            return SCALES.x(d.week + 0.5);
        })
        .attr("y", function(d) {

            return SCALES.y(d.rank - 1);
        })
        .attr("dy", "0.35em")
        .attr("text-anchor", "middle")
        .style('opacity', 0.0)
        .text(function(d) {
            return d.rank
        })
        .on('mouseover', function(d) {

            highlight(vis, d.name);
        })
        .on('mouseout', function() {

            unhighlight(vis);
        });
}

// Add offset markers.
//
// vis: the visualization root.
// data: marker data.
// class: marker sub-class.
//
function addOffsetMarkers(vis, data, cssClass) {

    // Place circle glyph.
    vis.selectAll("circle.marker." + cssClass)
        .data(data)
        .enter()
        .append("svg:circle")
        .attr("class", "marker " + cssClass + " zoom")
        .attr("cx", function(d) {

            return SCALES.x(d.week + 0.5);
        })
        .attr("cy", function(d) {

            return SCALES.y(d.rank - 1);
        })
        .attr("r", 0.6*MARKER_RADIUS)
        .style("fill", function(d) {

            return SCALES.clr(d.start);
        })
        .on('mouseover', function(d) {

            highlight(vis, d.name);
        })
        .on('mouseout', function() {

            unhighlight(vis);
        });
}

// Gets the window dimensions.
//
function getWindowDimensions() {

    var width = 940;
    var height = 640;
//     if (document.body && document.body.offsetWidth) {
// 
//         width = document.body.offsetWidth;
//         height = document.body.offsetHeight;
//     }
// 
//     if (document.compatMode == 'CSS1Compat' && document.documentElement && document.documentElement.offsetWidth) {
// 
//         width = document.documentElement.offsetWidth;
//         height = document.documentElement.offsetHeight;
//     }
// 
//     if (window.innerWidth && window.innerHeight) {
// 
//         width = window.innerWidth;
//         height = window.innerHeight;
//     }

    return {'width': width, 'height': height};
}
