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