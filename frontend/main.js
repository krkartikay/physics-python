var s = io("http://localhost:5000");
var t = 0;
var curdata = {};
var w = window.innerWidth;
var h = window.innerHeight;

function setup() {
    s.emit("particle", [1, 0, 1], [3, 0, 5], 1);
    loop();
}

function loop() {
    s.emit("data", (data) => {
        curdata = data;
        drawdata(data);
    });
    s.emit("step");
    t += 1;
    requestAnimationFrame(loop);
}

function stop() {
    clearInterval(intervalId);
}

$(setup);

// ---------------------------------------------------------------------------

function drawdata(data) {
    var xscale = d3.scaleLinear()
        .domain([-30, 30])
        .range([0, w]);
    var yscale = d3.scaleLinear()
        .domain([-20, 20])
        .range([h, 0]);
    var circles = d3.select("#draw")
        .selectAll("circle")
        .data(data.particles);
    circles
        .enter()
        .append("circle")
        .attr("class", "particle")
    circles
        .attr("cx", (d) => xscale(d.pos[0]))
        .attr("cy", (d) => yscale(d.pos[2])) // temporary workaround TODO -- set up some 3d projection
        .attr("r", (d) => (d.mass * 10));
}