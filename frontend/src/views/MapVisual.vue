<template>
  <div id="leaflet_map">
    <div style="height: 100vh; width: 100%">
      <LMap id="mymap" :zoom="zoom" :center="center">
      <LTileLayer :url="url" :attribution="attribution"></LTileLayer>
      <!-- <LGeoJson :geojson="geojson"></LGeojson> -->
      <LMarker id="sydney"
        :lat-lng="[-33.8688,151.2093]"
         @click="changeCenter([[-33.8688,151.2093],'Sydney'])"></LMarker>
      <LMarker id="melbourne"
        :lat-lng="[-37.8136,144.9631]"
        @click="changeCenter([[-37.8136,144.9631],'Melbourne'])"></LMarker>
      <LMarker id="brisbane"
        :lat-lng="[-27.4705,153.0260]"
        @click="changeCenter([[-27.4705,153.0260],'Brisbane'])"></LMarker>
      <LMarker id="perth" 
        :lat-lng="[-31.9523,115.8613]"
        @click="changeCenter([[-31.9523,115.8613],'Perth'])"></LMarker>
      <LMarker id="adelaide" 
        :lat-lng="[-34.9285,138.6007]"
        @click="changeCenter([[-34.9285,138.6007],'Adelaide'])"></LMarker>
      </LMap>
    </div>
    

    <div id="onmap">
      <div class="container mt-3">
        <h2>Choose City and Date</h2>
        <div class="row" style="width: 100vw;">
          <div style="margin-left: 10px;">
              <a class="navbar-brand font-weight-bold">Date: </a>
          </div>
          <div style="margin-left: 10px;">
            <span class="pull-left">
              <datetime v-model="date" 
                :type="date" 
                :format="{year: 'numeric', month: 'numeric', day: 'numeric'}" 
                :title="'Select the date you want'"
                @click="getData()"
                ></datetime>
            </span>
          </div>
        </div>
        <div class="row" style="width: 100vw;">
          <div style="margin-left: 10px;">
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
        <button id="dataButton" @click="getData()">Search</button>  
      </div>
      <br/>
      <div></div>
    </div>

    <div id="onmap2"  v-if="visible">    
      <div class="info">
        <p></p>
        <div v-html="dataText"></div>
      </div> 
      <br/>     
    </div>

    <a class="anchor" id="anchor1"></a>
    <!-- <nav class="navbar fixed-bottom navbar-light"> -->
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
              <!-- <b-dropdown-item @click="changeCenter([[-37.8136,144.9631],'Melbourne'])">Melbourne</b-dropdown-item>
              <b-dropdown-item @click="changeCenter([[-33.8688,151.2093],'Sydney'])">Sydney</b-dropdown-item>
              <b-dropdown-item @click="changeCenter([[-27.4705,153.0260],'Brisbane'])">Brisbane</b-dropdown-item>
              <b-dropdown-item @click="changeCenter([[-31.9523,115.8613],'Perth'])">Perth</b-dropdown-item>
              <b-dropdown-item @click="changeCenter([[-34.9285,138.6007],'Adelaide'])">Adelaide</b-dropdown-item> -->
            </b-dropdown>
      </div>
      <div style="margin-left: 10px;">
        <span class="pull-left">
          <p class="city" v-text="areaText"></p>
        </span>
      </div>
      <div style="margin-left: 10px;">
        <span class="pull-left">
          <button id="search-button" @click="getData()">search</button>
        </span>
      </div>
      <div style="margin-left: 10px;">
        <span class="pull-left">
          <p class="data" v-text="dateText"></p>
        </span>
      </div>
    </div>
    <!-- </nav> -->

    <!-- Charts -->
    <div id="chart" class="container-fluid w-100 d-inline-block" style="height: 100vh;z-index:0;">
      <div class="row">
        <div class="col-lg-12"><Linechart :chartData="this.lineDatacollection" :height="700" :width="2000" /></div>
      </div> 
    </div>

    <div class="row" style="width: 100vw;">
      <div style="margin-left: 30px;">
          <a class="navbar-brand font-weight-bold">Aurin: </a>
      </div>
      <div style="margin-left: 30px;">
              <b-dropdown id="dropdown-1" text="Aurin">
              <b-dropdown-item @click="changeAurin('edu')">Education</b-dropdown-item>
              <b-dropdown-item @click="changeAurin('income')">Income</b-dropdown-item>
              <b-dropdown-item @click="changeAurin('emp')">Employment Rate</b-dropdown-item>
              <b-dropdown-item @click="changeAurin('unemp')">Unemployment Rate</b-dropdown-item>
            </b-dropdown>
      </div>
      <div style="margin-left: 10px;">
        <span class="pull-left">
          <p class="city" v-text="infoText"></p>
        </span>
      </div>
    </div>
    <div id="chart" class="container-fluid w-100 d-inline-block" style="height: 100vh;z-index:0;">
      <div class="row">
        <div class="col-lg-12"><Barchart :chartData="this.barDatacollection" :height="700" :width="2000" /></div>
      </div> 
    </div>  
  </div>
  
</template>

<script>
import { LMap, LTileLayer, LMarker, LGeoJson } from "vue2-leaflet"
import Linechart from './../components/Linechart'
// import Linechart from './../components/Lineardemo'
import Barchart from './../components/Barchart'
import 'bootstrap/dist/css/bootstrap.css'
import {Datetime} from 'vue-datetime'
import 'vue-datetime/dist/vue-datetime.css'
export default {
  name: "Map",
  components: {
    LMap,
    LTileLayer,
    // LGeoJson,
    LMarker,
    Linechart,
    Barchart,
    datetime: Datetime,
  },
  data() {
    return {
      url:'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution:'&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      center: [-28.2744,133.7751],
      zoom: 5,
      bounds: null,
      date: new Date().toString(),
      lineDatacollection: null,
      barDatacollection: null,
      visible: false,
      // geojson: null,
      areaText: 'Australia',
      infoText: '',
      dataText: '',
      dateText: '',
      cities: []
    };
  },
  methods: {
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
    // getData(){
    //   this.seen = true;
    //   if (this.areaText == 'Australia')
    //     this.dataText = '<b>Please choose a city</b>'
    //   else if (this.date == '')
    //     this.dataText = '<b>Please choose a date</b>'
    //   else
    //     this.changeCenter(this.center,this.dataText);
    // },

    changeCenter(type) {
      this.visible = false; 
      this.center = L.latLng(type[0]);
      this.areaText = type[1];
    },

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
        console.log('res: ', res)
        this.dataText = '<h4>Data Statistic</h4>'
        +'<h5>'+type[1]+'</h5>'
        +'<b> Sentiment:'+ res.data.sentiment.toFixed(4) +'</b><br/>'
        +'<b> Total tweets:'+ res.data.count +'</b><br/>'
        +'<b> Positive tweets:'+ res.data.positive +'</b><br/>'
        +'<b> Nagetive tweets:'+ res.data.negative +'</b><br/>'
        +'<b> Educatin:'+ res.data.edu +'</b><br/>'
        +'<b> Income:'+ res.data.income +'</b><br/>'
        +'<b> Employment:'+ res.data.emp +'</b><br/>'
        +'<b> Unemployment:'+ res.data.unemp +'</b><br/>'; 
      })
      .catch(error => {
        console.error(error)
      })
  

      this.$ajax({
        url: 'api/get_dogcoin_price',
        method: 'POST',
        data: {
          city: type[1],
          date: time
        }
      }).then(res => {
        console.log('res: ', res)
        console.log('key: ', Object.keys(res.data.sen_hourly))
        console.log('value: ', Object.values(res.data.sen_hourly))
        var sen_data_tmp = Object.values(res.data.sen_hourly);
        var sen_data = new Array();
        for (let i in sen_data_tmp){
          sen_data[i] = (sen_data_tmp[i] / 1000).toFixed(4);
        }
        this.lineDatacollection = {
          labels: Object.keys(res.data.sen_hourly),
          datasets: [
            {
              label: 'sentiment(*10^3)',
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
              data: Object.values(res.data.dogcoin_price_hourly),
            }
          ]
        }
      })
      .catch(error => {
        this.visible = false,
        this.flash(`${error}`, 'error'),
        this.errored = true
      })
    },

    changeAurin(type) {
      let sdate = new Date(this.date);
      let time = this.formatChanger(sdate);
      if (this.date == '')
        this.infoText = 'Please choose a date.'
      else
        this.infoText = type
  
      this.$ajax({
        url: 'api/bar',
        method: 'POST',
        data: {
          date: time
        }
      }).then(res => {
        console.log('res: ', res)
        console.log('key: ', Object.keys(res.data[type]))
        var aurin_data_tmp = Object.values(res.data[type]);
        var aurin_data = new Array();
        for (let i in aurin_data_tmp){
          aurin_data[i] = (aurin_data_tmp[i] / 1000000);
        }
        this.barDatacollection = {
          labels: Object.keys(res.data.ave_sen),
          datasets: [
            {
              label: 'sentiment(*10^6)',
              borderColor: 'blue',
              backgroundColor: 'blue',
              data: Object.values(res.data.ave_sen),
            },
            {
              label: 'aurin',
              borderColor: 'red',
              backgroundColor: 'red',
              data: aurin_data,
            }
          ]
        }
      })
      .catch(error => {
        this.visible = false,
        this.errored = true
        console.log(error)
      })
    },
    showdata() {
      let sdate = new Date(this.date);
      let time = this.formatChanger(sdate);
      this.dateText = time;
    },
    // =========================== Time formatter ================================
    formatChanger(date) {
      let off = date.getTimezoneOffset();
      off = Math.abs(off);

      return date.getFullYear() + '-' + (date.getMonth()+1) + '-' +
            date.getDate(); 
    },
  },
  // async created () {
  //   const response = await fetch('melbourne.geojson');
  //   this.geojson = await response.json();
  // },
  mounted () {
    this.getCities();
    // this.setupMap();
    // this.chartBuildMachine();
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
  top: 80px; 
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
  top: 80px; 
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
}
.info h4 {
    margin: 0 0 5px;
    color: #777;
}
.info h5 {
    margin: 0 0 5px;
    color: #777;
}
.info b {
    color: #777;
}
</style>