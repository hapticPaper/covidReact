//height='50vh' width='50vw'  

function cvheight() {return Math.max(520, window.innerHeight/2)}
function cvwidth() {return Math.max(404, window.innerWidth/2)}


function resizeCanvas(){
    let canvas = document.getElementById('svgcanvas')
    canvas.setAttribute('height', `${cvheight()}px`)
    canvas.setAttribute('width', `${cvwidth()}px`)
}

window.addEventListener('resize', resizeCanvas)
resizeCanvas()

var scaleLongitude = d3.scaleLinear()
.domain([-135, -70])  //65 * 8
.range([0, 520]);

var scaleLatitude = d3.scaleLinear()
.domain([20, 60])  //40 * 10.1
.range([404, 0]);

function makeCircle(cx,cy, r){
cid = `circle-${cx}${cy}${parseInt(Math.random()*10000)}`
cir = document.createElementNS("http://www.w3.org/2000/svg", "circle")
cir.setAttribute('id', cid)
cir.setAttribute('cx', cx)
cir.setAttribute('cy', cy)
cir.setAttribute('r', 0)
cir.style.fill = 'rgb(100, 10,10)'
cir.style.stroke = 'rgb(100, 10,10)'
cir.style.opacity=0.2
cir.setAttribute('stroke-width', 1);
death = document.getElementById("svgcanvas");
death.appendChild(cir)

d3.select(`#${cid}`)
.transition().duration(2500).attr('r', Math.round(Math.log(r)))
};

function plotUSA(lat, lng, r){
py = Math.round(scaleLatitude(lat))
px = Math.round(scaleLongitude(lng))
console.log(`${px},${py}, ${r}`)
makeCircle(px, py, r)
}

covidData.forEach(d=>{plotUSA(d.lat, d.lng, d.confirmed)})
d3.select(`f1`)
.transition().duration(500).attr('color','red')