import Vue from 'vue'
import Router from 'vue-router'
import Map from '@/views/MapVisual.vue'

Vue.use(Router)

// const Map = () => import('@/views/MapVisual.vue')

export default new Router({
  routes: [{
    path: '/map',
		component: Map,
  }],
	mode: 'history'
})