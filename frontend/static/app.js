fetch('/latestCovid').then(d=>d.json()).then(data=>{
    tbl = document.getElementById('statsTable')
    tbl.innerHTML="<thead><tr><th>Locale</th><th>Confirmed</th><th>Deaths</th></thead>"
    data.results.forEach(city => { 
        tr = document.createElement('tr')
        td1 = document.createElement('td')
        td2 = document.createElement('td')
        td3 = document.createElement('td')
        td1.innerHTML= `<b>${city.locale}</b>`
        td2.innerHTML= `${city.confirmed}`
        td3.innerHTML= `${city.deaths}`
        tr.appendChild(td1)
        tr.appendChild(td2)
        tr.appendChild(td3)
        tbl.appendChild(tr);
    });
})