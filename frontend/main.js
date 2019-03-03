var s = io("http://localhost:5000");
var t = 0;
var curdata = {};
var w = window.innerWidth;
var h = window.innerHeight;
var running = true;

var xScale = d3.scaleLinear()
    .domain([-30, 30])
    .range([0, w]);
var yScale = d3.scaleLinear()
    .domain([-20, 20])
    .range([h, 0]);
var massScale = d3.scaleLinear()
    .domain([0, 10])
    .range([0, 50]);

// ===========================================================================

function initPhysics() {
    // s.emit("particle", [0, 0, 0], [2.5, 0, 5], 1);
    s.emit("init");
}

// ---------------------------------------------------------------------------

function drawdata(data) {
    var circles = d3.select("#draw")
        .selectAll("circle")
        .data(data.particles);
    circles
        .enter()
        .append("circle")
        .attr("class", "particle")
    circles
        .attr("cx", (d) => xScale(d.pos[0]))
        .attr("cy", (d) => yScale(d.pos[2]))
        .attr("r", (d) => massScale(d.mass));
    var springs = d3.select("#draw")
        .selectAll("line.spring")
        .data(data.springs);
    springs
        .enter()
        .append("line")
        .attr("class", "spring");
    springs
        .attr("x1", (d) => xScale(d.p1[0]))
        .attr("x2", (d) => xScale(d.p2[0]))
        .attr("y1", (d) => yScale(d.p1[2]))
        .attr("y2", (d) => yScale(d.p2[2]))
        .attr("stroke", "#fff");
    // TODO later on add code to show results in 3D
}

// ---------------------------------------------------------------------------

function setup() {
    initDrawing();
    initPhysics();
    loop();
}


function initDrawing() {
    var xAxis = d3.axisBottom(xScale);
    var yAxis = d3.axisLeft(yScale);
    d3.select("#xAxis").call(xAxis).attr("transform", `translate(0,${h / 2})`);
    d3.select("#yAxis").call(yAxis).attr("transform", `translate(${w / 2},0)`);
}

function loop() {
    s.emit("data", (data) => {
        curdata = data;
        drawdata(data);
    });
    s.emit("step");
    t += 1;
    if (running) requestAnimationFrame(loop);
}

function stop() {
    running = false;
}

$(setup);