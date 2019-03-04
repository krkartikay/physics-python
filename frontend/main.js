var s = io("http://localhost:5000");
// use like: resp = await s.get("ping", "data")
s.get = function (event, ...payload) {
    return new Promise(function (resolve, reject) {
        return s.emit(event, ...payload, function (...args) {
            return resolve(...args);
        })
    })
}
// ============================================================================

var t = 0;
var data = {};
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

async function initPhysics() {
    await s.get("init", ["SpringForce", "GravityForce"])
    var parts = {};
    var max = 10;
    for (let i = -max + 1; i <= max - 1; i++) {
        var z = 0;
        // z = 5*Math.cos(i);
        parts[i] = await s.get("particle", [i, 0, 0], [0, 0, z], 1);
    }
    var p_first = await s.get("fixed_particle", [-max, 0, 0], 1);
    var p_last = await s.get("fixed_particle", [max, 0, 0], 1);
    parts[-max] = p_first;
    parts[max] = p_last;
    for (let i = -max; i < max; i++) {
        await s.get("spring", parts[i], parts[i+1], {"k":100, "damping": 5});
    }
}

// ---------------------------------------------------------------------------

function drawdata(data) {
    var circles = d3.select("#draw")
        .selectAll("circle")
        .data(data.particles);
    circles
        .enter()
        .append("circle")
        .attr("class", (d) => d.type == "fixed" ? "particle fixed" : "particle")
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

async function setup() {
    initDrawing();
    await initPhysics();
    loop();
}


function initDrawing() {
    var xAxis = d3.axisBottom(xScale);
    var yAxis = d3.axisLeft(yScale);
    d3.select("#xAxis").call(xAxis).attr("transform", `translate(0,${h / 2})`);
    d3.select("#yAxis").call(yAxis).attr("transform", `translate(${w / 2},0)`);
}

async function loop() {
    data = await s.get("data");
    if(data) drawdata(data);
    s.emit("step", 10);
    t += 1;
    if (running) requestAnimationFrame(loop);
}

function stop() {
    running = false;
}

$(setup);