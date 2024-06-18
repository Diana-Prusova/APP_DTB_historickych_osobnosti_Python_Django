// zobrazení mapy Leaflet (nezapomenout na CSS v head)
var map = L.map('map').setView([50, 40], 3);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 8,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// načtení dat z JSON
let data = JSON.parse(document.getElementById('data_json').textContent);

// vytvoření markerů
data.forEach(one => {
    L.marker([one.latitude, one.longitude]).addTo(map)
        .bindPopup(`<a href="${one.detail_url}">${one.jmeno}</a>`);
}
    
)