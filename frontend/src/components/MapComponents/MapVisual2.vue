<template>
  <div style="height: 80vh">
    <LMap :zoom="zoom" :center="center">
      <LTileLayer :url="url"></LTileLayer>
      <LMarker :lat-lng="[-37.81361,144.96306]"></LMarker>
      <LMarker :lat-lng="[-37.81361,144.95306]"></LMarker>
      <LMarker :lat-lng="[-37.82361,144.96306]"></LMarker>
      <LMarker :lat-lng="[-37.81861,144.962661]"></LMarker>
    </LMap>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
export default {
  name: "Map",
  components: {
    LMap,
    LTileLayer,
    LMarker
  },
  data() {
    return {
      url: "https://{s}.tile.osm.org/{z}/{x}/{y}.png",
      zoom: 10,
      center: [-37.81361,144.96306],
      bounds: null
    };
  }
};
</script>