// ==========================
// COMP90024 Assignment 2
// Team: 38
// City: Melbourne
// Members:
// Ziran Gu (1038782)
// Jueying Wang (1016724)
// Yifei Zhou(980429)
// Jiakai Ni (988303)
// Ziyue Liu (1036109)
// ==========================
<template>
  <div id="leaflet_map">
    <!-- Interactive Map -->
    <div style="height: 100vh; width: 100%;">
      <l-map id="mymap" 
        :zoom="zoom"  
        :center="center">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-control-zoom position="topleft"></l-control-zoom>
      <l-marker id="sydney"
        :lat-lng="[-33.8688,151.2093]"
         @click="changeCenter([[-33.8688,151.2093],'Sydney'])"></l-marker>
      <l-marker id="melbourne"
        :lat-lng="[-37.8136,144.9631]"
        @click="changeCenter([[-37.8136,144.9631],'Melbourne'])"></l-marker>
      <l-marker id="brisbane"
        :lat-lng="[-27.4705,153.0260]"
        @click="changeCenter([[-27.4705,153.0260],'Brisbane'])"></l-marker>
      <l-marker id="perth" 
        :lat-lng="[-31.9523,115.8613]"
        @click="changeCenter([[-31.9523,115.8613],'Perth'])"></l-marker>
      <l-marker id="adelaide" 
        :lat-lng="[-34.9285,138.6007]"
        @click="changeCenter([[-34.9285,138.6007],'Adelaide'])"></l-marker>
      </l-map>
    </div>
    

    <div id="onmap">
      <!-- Search Box on Map -->
      <div class="container mt-3">
        <h2>Choose City and Date</h2>
        <div class="row" style="width: 100vw;">
          <div style="margin-left: 15px;">
              <a class="navbar-brand font-weight-bold" style="text-align: right">Date: </a>
          </div>
          <div style="margin-left: 5px;">
            <span class="pull-left">
              <datetime v-model="date" 
                :type="date" 
                :format="{year: 'numeric', month: 'numeric', day: 'numeric'}" 
                :title="'Select the date you want'"
                @click="setVisible()"
                ></datetime>
            </span>
          </div>
        </div>
        <div class="row" style="width: 100vw;">
          <div style="margin-left: 15px;">
            <b-dropdown id="dropdown-1" text="City">
              <b-dropdown-item
                v-for="city in cities"
                :key="city.city_name"
                @click="changeCenter([city.position,city.city_name])">
                {{ city.city_name }}
              </b-dropdown-item>
            </b-dropdown>
          </div>
          <div style="margin-left: 5px;">
            <span class="pull-left">
              <p class="city" v-text="areaText"></p>
            </span>
          </div>
        </div>
        <br/>
        <button class="btn btn-dark" style="margin-left:180px" @click="getData()">Search</button>  
      </div>
      <br/>
      <div></div>
    </div>

    <div id="onmap2"  v-if="visible">
      <!-- Overall Data on Map -->    
      <div class="info">
        <p></p>
        <div v-html="dataText"></div>
        <br/>
        <div v-text="warnText"></div>
      </div> 
      <br/>     
    </div>

    <a class="anchor" id="anchor1"></a>
    <br/>
    <div id="chart_visual" v-if="seen">
      <div></div>
      <!-- Search Bar above Line Chart -->
      <div class="row" style="width: 100vw;">
        <div style="margin-left: 30px;">
            <a class="navbar-brand font-weight-bold">Date: </a>
        </div>
        <div style="margin-left: 10px;">
          <span class="pull-left">
            <datetime v-model="date" 
              :type="date" 
              :format="{year: 'numeric', month: 'numeric', day: 'numeric'}" 
              :title="'Select the date you want'"
              ></datetime>
          </span>
        </div>
        <div style="margin-left: 30px;">
              <b-dropdown id="dropdown-1" text="City">
                <b-dropdown-item
                  v-for="city in cities"
                  :key="city.city_name"
                  @click="changeCenter([city.position,city.city_name])">
                  {{ city.city_name }}
                </b-dropdown-item>
              </b-dropdown>
        </div>
        <div style="margin-left: 10px;">
          <span class="pull-left">
            <p class="city" v-text="areaText"></p>
          </span>
        </div>
        <div style="margin-left: 10px;">
          <span class="pull-left">
            <button class="btn btn-dark" @click="getData()">search</button>
          </span>
        </div>
        <div style="margin-left: 10px;">
          <span class="pull-left">
            <p class="warning" v-text="warning"></p>
          </span>
        </div>
      </div>
      <!-- Charts -->
      <div id="chart" class="container-fluid w-80 d-inline-block" style="height: 50vh">
        <div class="row">
          <div class="col-lg-12"><Linechart :chartData="this.lineDatacollection" :height="700" :width="2000" /></div>
        </div>
        <br/>
        <div class="row" style="width: 100vw;">
          <div style="margin-left: 30px;">
              <a class="navbar-brand font-weight-bold">Aurin: </a>
          </div>
          <div style="margin-left: 30px;">
                  <b-dropdown id="dropdown-1" text="Aurin">
                  <b-dropdown-item @click="changeAurin(['edu','Education'])">Education</b-dropdown-item>
                  <b-dropdown-item @click="changeAurin(['income','Income'])">Income</b-dropdown-item>
                  <b-dropdown-item @click="changeAurin(['emp','Employment'])">Employment Rate</b-dropdown-item>
                  <b-dropdown-item @click="changeAurin(['unemp','Unemployment'])">Unemployment Rate</b-dropdown-item>
                </b-dropdown>
          </div>
          <div style="margin-left: 10px;">
            <span class="pull-left">
              <p class="city" v-text="infoText"></p>
            </span>
          </div>  
        </div>
        <div id="chart" class="container-fluid w-100 d-inline-block" style="height: 50vh">
          <div class="row">
            <div class="col-lg-12"><Barchart :chartData="this.barDatacollection" :height="700" :width="2000"/></div>
          </div> 
        </div>  
      </div>
    </div>
  </div>
  
</template>

<script>
import { LMap, LTileLayer, LMarker, LControlZoom} from "vue2-leaflet"
import Linechart from './../components/Linechart'
import Barchart from './../components/Barchart'
import 'bootstrap/dist/css/bootstrap.css'
import {Datetime} from 'vue-datetime'
import 'vue-datetime/dist/vue-datetime.css'
export default {
  name: "Map",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LControlZoom,
    Linechart,
    Barchart,
    datetime: Datetime,
  },
  data() {
    return {
      url:'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:'&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      center: [-28.2744,133.7751],
      zoom: 5,
      mapOptions: {
        zoomSnap: 0.5
      },
      bounds: null,
      date: new Date().toString(),
      lineDatacollection: null,
      barDatacollection: null,
      visible: false,
      seen: false,
      areaText: 'Australia',
      infoText: '',
      dataText: '',
      warning: '',
      warnText: '',
      cities: []
    };
  },
  methods: {
    // ================== Get city info from backend ==================
    getCities() {
      this.$ajax({
        url: 'api/get_cities',
        method: 'POST',
        data: {}
      }).then(res => {
        const { cities } = res.data
        this.cities = cities.map(({ city_name, position }) => {
          const position_with_name = position.push(city_name)
          return {
            city_name,
            position
          }
        })
      }).catch(e => {
        console.error(e)
      })
    },

    // =========================== Change Map Center ================================
    changeCenter(type) {
      this.visible = false; 
      this.center = L.latLng(type[0]);
      this.areaText = type[1];
    },

    // ============= Check whether the data in search box is available ==============
    getData() {
      this.visible = true;
      if (this.date == '' && this.areaText == 'Australia')
        this.dataText = '<b>Please choose city and date</b>'
      else if (this.date == '' && this.areaText != 'Australia')
        this.dataText = '<b>Please choose a date</b>'
      else if (this.date != '' && this.areaText == 'Australia')
        this.dataText = '<b>Please choose a city</b>'
      else
        this.dataStatistic([this.center,this.areaText]);
    },

    // =========================== Get Overall Data ================================
    dataStatistic(type) {   
      let sdate = new Date(this.date);
      let time = this.formatChanger(sdate);
      this.$ajax({
        url: 'api/get_data_statistic',
        method: 'POST',
        data: {
          city: type[1],
          date: time
        }
      }).then(res => {
        this.seen = true;
        console.log('res: ', res)
        if (res.data != 'No data') {
          this.dataText = '<h4>Data Statistic</h4>'
          +'<h5>'+type[1]+'</h5>'
          +'<b> Sentiment:'+ res.data.sentiment.toFixed(4) +'</b><br/>'
          +'<b> Total tweets:'+ res.data.count +'</b><br/>'
          +'<b> Positive tweets:'+ res.data.positive +'</b><br/>'
          +'<b> Nagetive tweets:'+ res.data.negative +'</b><br/>'
          +'<b> Educatin(%):'+ res.data.edu +'</b><br/>'
          +'<b> Income:'+ res.data.income +'</b><br/>'
          +'<b> Employment(%):'+ res.data.emp +'</b><br/>'
          +'<b> Unemployment(%):'+ res.data.unemp +'</b><br/>';
          this.warning = '';
          this.warnText = '';
          this.initChart([type[1],time]);
        } else {
          this.seen = false;
          this.dataText = '<p>Sorry! We does not count the data of the day, please choose another date (5/5/2021 - 24/5/2021).</p>';
          this.warning =  'Sorry! We does not count the data of the day, please choose another date.';
        }  
      })
      .catch(error => {
        this.seen = false;
        console.error(error)
      })
    },

    // ================= Get Line Chart Data and Initial Chart======================
    initChart(type) {
      this.seen = true;
      this.$ajax({
        url: 'api/get_dogcoin_price',
        method: 'POST',
        data: {
          city: type[0],
          date: type[1]
        }
      }).then(res => {
        console.log('res: ', res)
        if (res.data == 'No data'){
          this.seen = false;
          this.warnText = 'Sorry! We does not count dogecoin price of the day, please choose another date (5/5/2021 - 24/5/2021).'
        } else {
          var sen_data = Object.values(res.data.sen_hourly);
          this.lineDatacollection = {
            labels: Object.keys(res.data.sen_hourly),
            datasets: [
              {
                label: 'sentiment',
                fill: false,
                tension: 0,
                borderColor: 'blue',
                backgroundColor: 'blue',
                data: sen_data,
              },
              {
                label: 'dogecoin(AU$)',
                fill: false,
                tension: 0,
                borderColor: 'red',
                backgroundColor: 'red',
                data: Object.values(res.data.dogcoin_price_hourly)
              }
            ]
          } 
        }
        
      })
      .catch(error => {
        this.seen = false;
        console.error(error)
      })
    },

    // ================= Get Aurin Data and Initial Bar Chart======================
    changeAurin(type) {
      let sdate = new Date(this.date);
      let time = this.formatChanger(sdate);
      if (this.date == '')
        this.infoText = 'Please choose a date.'
      else
        this.infoText = type[1]
  
      this.$ajax({
        url: 'api/bar',
        method: 'POST',
        data: {
          date: time
        }
      }).then(res => {
        console.log('res: ', res)
        var aurin_data_tmp = Object.values(res.data[type[0]]);
        var aurin_data = new Array();
        let aurin_label = type[1]
        if (type[0] == 'emp' || type[0] == 'unemp' || type[0] == 'edu') {
          for (let i in aurin_data_tmp){
            aurin_data[i] = (aurin_data_tmp[i] / 100);
          }
        } else {
          for (let i in aurin_data_tmp){
            aurin_data[i] = (aurin_data_tmp[i] / 1000000);
          }
          aurin_label = aurin_label + ' (million AU$)'
        }
        this.barDatacollection = {
          labels: Object.keys(res.data.ave_sen),
          datasets: [
            {
              label: 'sentiment',
              borderColor: 'blue',
              backgroundColor: 'blue',
              data: Object.values(res.data.ave_sen),
            },
            {
              label: aurin_label,
              borderColor: 'red',
              backgroundColor: 'red',
              data: aurin_data,
            }
          ]
        }
      })
      .catch(error => {
        console.log(error)
      })
    },
    
    // =========================== Time formatter ================================
    formatChanger(date) {
      let off = date.getTimezoneOffset();
      off = Math.abs(off);

      return date.getFullYear() + '-' + (date.getMonth()+1) + '-' +
            date.getDate(); 
    },
  },
  mounted () {
    this.getCities();
  },
};
</script>

<style>
@import '~bootstrap/dist/css/bootstrap.css';
@import '~bootstrap-vue/dist/bootstrap-vue.css';

#header #logo {
  background: url("../assets/images/logo.png") center;
  background-size: contain;
  background-repeat: no-repeat;
  background-color: transparent;
  position: fixed;
  width: 12em;
  height: 6em;
  top: 0;
  left: 1em;
}
#leaf_letmap {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
  background-color:#bbb;
  position: relative;
}
#onmap {
  background: rgba(255,255,255,0.8);
  box-shadow: 0 0 15px rgba(0,0,0,0.2);
  border-radius: 5px;
  position: absolute; 
  top: 100px; 
  left: 50px; 
  z-index: 9999; 
  border-radius: 25px;
  width: 280px;
}
#onmap h2 {
  text-align: center;
}
#onmap2 {
  background: rgba(255,255,255,0.8);
  box-shadow: 0 0 15px rgba(0,0,0,0.2);
  border-radius: 5px;
  position: absolute; 
  top: 100px; 
  right: 20px; 
  z-index: 9998; 
  border-radius: 25px;
  width: 320px;
}
.row {
  margin-top: 20px;
}
.city {
  padding-left: 15px;
  font-size: 1.5em;
}
.warning {
  padding-left: 15px;
  font-size: 1.5em;
}
a.anchor {
  display: block;
  position: relative;
  top: -6em;
  visibility: hidden;
}
.info {
    top: 70px;
    padding: 6px 8px;
    font: 14px/16px Arial, Helvetica, sans-serif;
    color: #777;
}
.info h4 {
    margin: 0 0 5px;
    
}
.info h5 {
    margin: 0 0 5px;
    
}
</style>