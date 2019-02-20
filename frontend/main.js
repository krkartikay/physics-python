s = io("http://localhost:5000");

s.emit("particle", [0, 0, 0], [1, 0, 10], 1);

i = 0

while(i < 100){
    s.emit("data", (data) => console.log(data.p1.pos));
    s.emit("step");
    i += 1
}