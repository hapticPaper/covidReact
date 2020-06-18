
function loadpage(){
    fetch('/atlasCovid').then(d=>d.json()).then(data=>{
        tbl = document.getElementById('statsTable')
        tbl.innerHTML="<thead><tr><th>Locale</th><th>Confirmed</th><th>Deaths</th></thead>"
        data.results.forEach(city => { 
            tr = document.createElement('tr')
            td1 = document.createElement('td')
            td2 = document.createElement('td')
            td3 = document.createElement('td')
            td1.innerHTML= `<b>${city.locale}</b>`
            td2.innerHTML= `${city.cases}`
            td2.style.width='110px'
            td3.innerHTML= `${city.deaths}`
            tr.appendChild(td1)
            tr.appendChild(td2)
            tr.appendChild(td3)
            tbl.appendChild(tr);
        });
       lr = document.getElementById('lastRefresh')
       d = new Date(0)
       d.setUTCSeconds(data.refreshed)
       lr.innerHTML=`${d}`
    });
}


function init(){
    resieImgs()
    loadpage()
    setInterval(loadpage, 15000)
    
}

init()


function resieImgs() {
    r = document.getElementById('cvimg')
    r.width=window.innerWidth*0.3
    r = document.getElementById('cvgif')
    r.width=window.innerWidth*0.45
  }
  
  window.onresize = resieImgs;