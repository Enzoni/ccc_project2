<template>
  <div id="home" v-if="this.$route.path == '/'">
    <!-- Introduction -->
    <section id="banner">
      <div class="inner">
        <!-- <div class="logo"></div> -->
        <p>
          COMP90024 - Cluster and Cloud Computing <br>
          Assignment Two <br>
          <br>
          Group 38
        </p>
      </div>
      <a href="#intro" class="more">Introduction</a>    
    </section>
    <section id="intro" class="wrapper center">
      <div class="inner">
        <h2>Project Introduction</h2>
        <p>This project is produced by group 38.</p>
        
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
