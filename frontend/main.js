var s = io("http://localhost:5000");
var t = 0;
var curdata = {};

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
    var circles = d3.select("#draw")
        .selectAll("circle")
        .data(data.particles);
    circles
        .enter()
        .append("circle")
        .attr("class", "particle")
    circles
        .attr("cx", (d) => (d.pos[0] * 100))
        .attr("cy", (d) => (d.pos[2] * 100)) // temporary workaround TODO
        .attr("r", (d) => (d.mass * 10));
}