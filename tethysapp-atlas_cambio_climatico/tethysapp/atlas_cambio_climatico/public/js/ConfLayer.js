function threeHoursAgo() {
    return new Date(Math.round(Date.now() / 3600000) * 3600000 - 3600000 * 3);
  }

var startDate = threeHoursAgo();  
var frameRate = 0.5; // frames per second
var animationId = null;
var monthNum = 1;
var maxNum = 12
var layerName = '';
var layersNum = 0;
const monthNames = ["Anual", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
];

function loadCCLayer(){
    var ol_map = TETHYS_MAP_VIEW.getMap();

    layersNum=ol_map.getLayers().getLength();
    getLayerName();
    monthNum = 1;
    if(layersNum >= 21){
        stop();
        ol_map.removeLayer(ol_map.getLayers().item(20));
    }
    

    var layera = new ol.layer.Tile({
        source: new ol.source.TileWMS({
        attributions: ['Jun'],
        url: 'http://localhost:8080/geoserver/wms',
        params: {'LAYERS': 'geoserver_app:CC_' + layerName + monthNum},
        serverType:'geoserver'
        }),
    });   
    ol_map.addLayer(layera);

    console.log('start');
    updateInfo();
 
    animationId = window.setInterval(setTime, 1000 / frameRate);
    
};

function getLayerName(){
    var e = document.getElementById('variable');
    layerName = e.options[e.selectedIndex].value;

    e = document.getElementById('unidadTemp');
    layerName += '_' + e.options[e.selectedIndex].value;

    e = document.getElementById('escenario');
    layerName += '_' + e.options[e.selectedIndex].value;

    e = document.getElementById('periodo');
    layerName += '_' + e.options[e.selectedIndex].value + '_';

    console.log(layerName);
};

function updateInfo() {
    var el = document.getElementById('info');
    
    e = document.getElementById('unidadTemp');
    if(e.options[e.selectedIndex].value == 'A'){
        monthNum = 0;
        maxNum=0;
    }
    else{
        maxNum=12;
    }

    el.innerHTML =  monthNames[monthNum];
    if(monthNum == maxNum){
        stop();
    }
}

function updateLayer(){
    var ol_map = TETHYS_MAP_VIEW.getMap();
    ol_map.getLayers().item(20).getSource().updateParams({'LAYERS': 'geoserver_app:CC_' + layerName + monthNum});
    updateInfo();
}

function setTime() {
    //var ol_map = TETHYS_MAP_VIEW.getMap();
    monthNum += 1;
    startDate.setMinutes(startDate.getMinutes() + 15);
    if (startDate > new Date()) {
        startDate = threeHoursAgo();
    }

   //console.log(ol_map.getLayers().item(20)); 
    //ol_map.getLayers().item(20).getSource().updateParams({'LAYERS': 'geoserver_app:CC_T_M_85_2070_'+monthNum});
    updateLayer();
    //updateInfo();
}

function stop() {
    // if (animationId !== null) {
    if (animationId != null) {
      window.clearInterval(animationId);
      animationId = null;
    }
    console.log('stop');
};

function backLayer() {
    if(monthNum > 1){
        stop();
        monthNum -= 1;
        updateLayer();
    }
};

function forwardLayer() {
    if(monthNum < 12){
        stop();
        monthNum += 1;
        updateLayer();
    }
};
// var play = function () {
//     stop();
//     animationId = window.setInterval(setTime, 1000 / frameRate);
// };