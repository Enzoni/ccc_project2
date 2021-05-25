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
  <div id='app' class="bg">
    <Navbar />
    <Home />
    <router-view></router-view>
  </div>
</template>


<script>
import Home from './views/Home'
import Navbar from './views/Navbar'

export default {
  name:"app",
  components: {
    Home,
    Navbar
  }
}
</script>


<style scoped src="./assets/styles/mystyles.css"></style>

