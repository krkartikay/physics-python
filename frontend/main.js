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
    await s.get("init", [["GravityForce", {"g": [0,0,1]}], "SpringForce", "DragForce"])
    var p1 = await s.get("particle", [0, 0, 0], [2, 0, 0], 1);
    var p2 = await s.get("fixed_particle", [0, 0, 5], 1);
    var sp = await s.get("spring", p1, p2, {"k":1000, "damping": 1});
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