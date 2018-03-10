<template>
  <v-card>
    <v-toolbar dense dark color="accent">
      <v-toolbar-title>Chart</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-menu bottom left>
        <v-btn slot="activator" flat dark>
          options
        </v-btn>
        <v-list>
          <v-list-tile min-width="200px">
            hi what's up
          </v-list-tile>
          <v-list-tile>
            <v-select
              :items="selectitems"
              v-model="options.series[0].type"
              label="Chart Type"
              single-line
              >
            </v-select>
          </v-list-tile>
        </v-list>
      </v-menu>
    </v-toolbar>
    <highcharts :options="options"></highcharts>
  </v-card>
</template>

<script>
export default {
  data () {
    return {
      selectitems: ['line', 'bar'],
      options: {
        series: [{
          type: 'line',
          data: [{'x': 1, 'y': 2}, {'x': 1, 'y': 4}]
        }]

      }
    }
  },
  watch: {
    datastart: function(newval, oldval) {
      this.getData(newval)
    }
  },
  methods: {
    getData(datastart) {
      this.$http.get('').then(response => {
        this.options.series = [{ data: response.body[0].slice(this.datastart) }]
      })
    }
  },
  props: ['datastart'],
  beforeMount() {
    this.getData()
  }
}
</script>

<style lang="scss">
</style>
