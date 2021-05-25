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

<script>
import { Bar, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  name:"Barchart",
  extends: Bar,
  mixins: [reactiveProp],
  props: [
    'height',
    'width',
    'chartData'
  ],
  mounted () {
    // Overwriting base render method with actual data.
    this.renderChart(this.chartData,{
      responsive: true,
      maintainAspectRatio: false 
    })
  }
}
</script>
