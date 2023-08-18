const myMap = L.map('mapid').setView([54.1003503, -3.3053616], 6);
const redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});
const blueIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const searchBtn = document.getElementById('searchBtn');
const resetBtn = document.getElementById('resetBtn');

const allBtns = [ searchBtn, resetBtn ];

// Initialize the buttons.
allBtns.map((b) => b.disabled = true);

let currentMarkers = [];
let searchResultMarkers = [];
let currentPolygon = null;

resetBtn.onclick = function () {
  if (currentPolygon) {
    myMap.removeLayer(currentPolygon);
    currentPolygon = null;
  }

  for (const marker of currentMarkers) {
    myMap.removeLayer(marker);
  }

  for (const marker of searchResultMarkers) {
    myMap.removeLayer(marker);
  }

  currentMarkers = [];
  searchResultMarkers = [];
  allBtns.map((b) => b.disabled = true);
};

searchBtn.onclick = async function () {
  // No need to check if there are enough points, as the 
  // button isn't clickable until there are.
  searchBtn.classList.add('is-loading');
  
  // Remove previous results.
  for (const marker of searchResultMarkers) {
    myMap.removeLayer(marker);
  }

  searchResultMarkers = [];

  try {
    // Call the search endpoint.
    const response = await fetch('/search', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        polygon: currentPolygon.toGeoJSON()
      })
    });

    const responseJSON = await response.json();
    // TODO do something!
  } catch (e) {
    console.log(e);
  }

  searchBtn.classList.remove('is-loading');
}

function updatePolygon() {
  if (currentMarkers.length > 2) {
    const polyCoords = currentMarkers.map((marker) => [ 
      marker.getLatLng().lat, 
      marker.getLatLng().lng 
    ]);

    if (currentPolygon) {
      myMap.removeLayer(currentPolygon);
    }
    
    currentPolygon = L.polygon(polyCoords, {color: 'red'}).addTo(myMap);
    allBtns.map((b) => b.disabled = false);
  }
}

L.tileLayer(
  'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', 
  {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }
).addTo(myMap);

myMap.on('click', (e) => {
  const newMarker = L.marker(e.latlng, { 
    icon: redIcon, 
    draggable: true 
  });

  newMarker.addTo(myMap);
  newMarker.on('move', () => updatePolygon());
  currentMarkers.push(newMarker);  
  updatePolygon();

  resetBtn.disabled = false;
});