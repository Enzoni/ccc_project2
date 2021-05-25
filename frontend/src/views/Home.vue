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
  <!-- Homepage -->
  <div id="home" v-if="this.$route.path == '/'">
    <section id="banner">
      <div class="inner">
        <p>
          COMP90024 - Cluster and Cloud Computing <br>
          Assignment Two <br>
          <br>
          Group 38
        </p>
      </div>
      <a href="#intro" class="more">Introduction</a>    
    </section>
    <!-- Project Introduction -->
    <section id="intro" class="wrapper center">
      <div class="inner">
        <h2>Project Introduction</h2>
        <p>Dogecoin (Currency symbol: Ð) is a virtual currency inherited from Litecoin 
          launched by IBM engineer Billy Markus. It was born on December 6, 2013.This 
          project is produced by group 38.  Our project will first obtain and display 
          Aurin data for five more populous cities in Australia (Melbourne, Sydney, 
          Brisbane, Perth and Adelaide), the Twitter of residents of these cities, and 
          the price of Dogecoin. Then through the comparative analysis of the three to 
          find whether there is a correlation between them.</p>
        <p class="button premium" onclick="window.location.href='/map'">
          <a id='premium'>Go to Statistic</a>
        </p>
      </div>
    </section>
  </div>
</template>


<script>
export default {
  name: "Home"
};
</script>


<style src="./../assets/styles/mystyles.css"></style>
<style>
#premium{
  color: black;
}
</style>
