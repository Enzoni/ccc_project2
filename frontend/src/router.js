import Vue from 'vue'
import Router from 'vue-router'
import Map from '@/view/Map.vue'

Vue.use(Router)

export default new Router({
  routes: [{
    path: '/',
    name: 'map',
    component: Map
  }],
	mode: 'history'
})