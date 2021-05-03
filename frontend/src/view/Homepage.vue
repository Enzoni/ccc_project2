<template>
  <div id="home" v-if="this.$route.path == '/'">
    <section id="banner">
      <div class="inner">
        <div class="logo"></div>
        <p>
          COMP90024 - Cluster and Cloud Computing <br>
          Assignment Two
        </p>
      </div>
      <a href="#intro" class="more">Learn More</a>    
    </section>
    <section id="intro" class="wrapper center">
      <div class="inner">
        <h2>Project Introduction</h2>
        <p class="button premium" onclick="window.location.href='/map'">
          <a id='premium'>Go Premium</a>
        </p>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Homepage',

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
p {
  color: black;
}
</style>