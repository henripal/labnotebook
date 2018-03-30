<template>
    <div id="graph"></div>
</template>

<script>
import Dygraph from 'dygraphs'

export default {
  data () {
    return {
        graph: null
    }
  },
  methods: {
    doNothing: function() {
    },
  },
  watch: {
      chartData: function(newVal, oldVal) {
          console.log('wazzup');
          this.graph.updateOptions({'file': newVal})
      }
  },
  mounted() {
    this.$nextTick(function() {
      this.graph = new Dygraph('graph',
      this.chartData,
         {
          fillGraph: true
      });
    })
  },
  props: {
      chartData: { default: [[1, 2], [3, 4]]}
  }
}
</script>

<style lang="scss">
</style>
