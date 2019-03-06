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

var frames = 0;
var data = {};
var w = window.innerWidth;
var h = window.innerHeight;
var running = true;
var zoom = 0.5;
var time = 0;
var timestep = 0.00025;

var xScale = d3.scaleLinear()
    .domain([-15 / zoom, 15 / zoom])
    .range([0, w]);
var yScale = d3.scaleLinear()
    .domain([-15 * (h / w) / zoom, 15 * (h / w) / zoom])
    .range([h, 0]);
var massScale = d3.scaleLinear()
    .domain([0, 10 / zoom])
    .range([0, 50]);

// ===========================================================================

// async function initPhysics() {
//     await s.get("init", timestep);
//     await s.get("add_force", "SpringForce")
//     await s.get("add_force", "ImpulsiveForce")
//     var parts = {};
//     var max = 25;
//     for (let i = -max + 1; i <= max - 1; i++) {
//         parts[i] = await s.get("particle", [i, 0, 0], [0, 0, 0], 1);
//     }
//     for (let x = 0; x <= 2*Math.PI/10; x += 0.01) {
//         await s.get("impulse", parts[-5],
//             {
//                 'start': x,
//                 'end': (x+0.01),
//                 'force': [0, 0, +500*Math.cos(10*x)]
//             }
//         );
//     }
//     var p_first = await s.get("fixed_particle", [-max, 0, 0], 1);
//     var p_last = await s.get("fixed_particle", [max, 0, 0], 1);
//     parts[-max] = p_first;
//     parts[max] = p_last;
//     for (let i = -max; i < max; i++) {
//         await s.get("spring", parts[i], parts[i + 1], { "k": 1000, "l": 0.25 });
//     }
// }

// ---------------------------------------------------------------------------

function drawdata(data, t) {
    var xScale = d3.scaleLinear()
        .domain([-15 / zoom, 15 / zoom])
        .range([0, w]);
    var yScale = d3.scaleLinear()
        .domain([-15 * (h / w) / zoom, 15 * (h / w) / zoom])
        .range([h, 0]);
    var massScale = d3.scaleLinear()
        .domain([0, 10 / zoom])
        .range([0, 50]);
    var circles = d3.select("#draw")
        .selectAll("circle")
        .data(data.particles);
    var springs = d3.select("#draw")
        .selectAll("line.spring")
        .data(data.springs);
    circles
        .enter()
        .append("circle")
        .transition()
        .attr("r", (d) => massScale(d.mass))
        .attr("class", (d) => d.type == "fixed" ? "particle fixed" : "particle")
    circles
        .attr("cx", (d) => xScale(d.pos[0] - 0.5 * d.pos[1]))
        .attr("cy", (d) => yScale(d.pos[2] - 0.5 * d.pos[1]))
        .attr("r", (d) => massScale(d.mass));
    springs
        .enter()
        .append("line")
        .style("opacity", "0.0")
        .transition()
        .style("opacity", "1.0")
        .attr("class", "spring");
    springs
        .attr("x1", (d) => xScale(d.p1[0] - 0.5 * d.p1[1]))
        .attr("y1", (d) => yScale(d.p1[2] - 0.5 * d.p1[1]))
        .attr("x2", (d) => xScale(d.p2[0] - 0.5 * d.p2[1]))
        .attr("y2", (d) => yScale(d.p2[2] - 0.5 * d.p2[1]))
        .attr("stroke", "#fff");
    circles
        .exit()
        .transition()
        .attr("r", 0.0)
        .remove();
    springs
        .exit()
        .transition()
        .style("stroke-opacity", "0")
        .remove();
    // TODO later on add code to show results in 3D
}

// ---------------------------------------------------------------------------

async function setup() {
    initDrawing();
    // await initPhysics();
    // loop();
    s.get("reload_file")
    replay_loop()
}


function initDrawing() {
    // var xAxis = d3.axisBottom(xScale);
    // var yAxis = d3.axisLeft(yScale);
    // d3.select("#xAxis").call(xAxis).attr("transform", `translate(0,${h / 2})`);
    // d3.select("#yAxis").call(yAxis).attr("transform", `translate(${w / 2},0)`);
}

function loop() {
    s.emit("step", 1, function (t) {
        s.emit("data", function (d) {
            data = d;
            drawdata(data, t);
            frames += 1;
            time += timestep;
            if (running) requestAnimationFrame(loop);
        });
    });
}

var realtime = 0;

// var log_interval = setInterval(() => {
//     console.log("t, fps: ", time, frames / 1);
//     frames = 0;
// }, 1000);

$(setup);

// ==============================================================================

function stop() {
    clearInterval(log_interval)
    running = false;
    s.get("reload_file");
}

var saved_data;

var ix = 0;

async function replay_loop() {
    data_ = await s.get("saved_data", ix);
    if (data_ == "restart") {
        drawdata({ 't': 0, "particles": [], "springs": [] });
        ix = 0;
        setTimeout(() => {
            requestAnimationFrame(replay_loop);
        }, 2000);
        return;
    } else {
        data = data_;
    }
    ix += 1;
    drawdata(data);
    requestAnimationFrame(replay_loop);
}

// stop();
// replay_loop();