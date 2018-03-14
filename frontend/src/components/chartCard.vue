<template>
  <v-card>
    <v-toolbar dense dark color="accent">
      <v-toolbar-title>Chart</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-menu bottom left min-width='250px' :close-on-content-click="false">
        <v-btn slot="activator" flat dark>
          options
        </v-btn>
        <v-list dense>
          <v-list-tile>
            <v-list-tile-content>
              <v-list-tile-title>
              Variables to plot: 
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile>
            <v-checkbox label='Val. Acc.' v-model="toplot" value="valacc"></v-checkbox>
          </v-list-tile>
          <v-list-tile>
            <v-checkbox label='Train. Acc.' v-model="toplot" value="trainacc"></v-checkbox>
          </v-list-tile>
          <v-list-tile>
            <v-checkbox label='Train. Loss' v-model="toplot" value="trainloss"></v-checkbox>
          </v-list-tile>
          <v-list-tile>
            <v-list-tile-content>
              <v-list-tile-title>
              Y-axis type: 
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile>
            <v-radio-group :column="false" v-model="options.yAxis.type">
              <v-radio label="log" value="logarithmic"></v-radio>
              <v-radio label="linear" value="linear"></v-radio>
            </v-radio-group>
          </v-list-tile>
          <v-list-tile>
            <v-list-tile-content>
              <v-list-tile-title>
              Streaming:
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile>
            <v-switch :label="'autoupdate ' + (liveUpdate ? 'on' : 'off')"
            v-model="liveUpdate"></v-switch>
          </v-list-tile>
        </v-list>
      </v-menu>
    </v-toolbar>
    <highcharts :options="options" ref="chart"></highcharts>
  </v-card>
</template>

<script>
export default {
  data () {
    return {
      liveUpdate: false,
      intervalControl: null,
      updateTime: 200,
      toplot: ['valacc'],
      selectitems: ['line', 'bar'],
      options: {
        chart: {
          zoomType: 'x'
        },
        yAxis: {
          title: {text: null },
          type: 'linear'
        },
        title: null,
        series: [{id: 'dummy', data: [null, null]}]
      }
    }
  },
  computed: {
    toplot_val: function() {
      return this.toplot;
    }
  },
  methods: {
    responseToData: function(response, seriesname) {
      var y = response.body[seriesname]
      var x = response.body.timestep

      return x.map((e, i) => { return [e, y[i]]})
    },
    addExperiment: function(experiment_id) {
      for (var tp of this.toplot) {
        this.addSeries(experiment_id, tp)
      }
    },
    addSeries: function(index, variable) {
      var dummy = this.$refs.chart.chart.get('dummy');
      if (dummy !== undefined) { dummy.remove(); }
      this.$http.get('steps/' + index).then(function(response) {
        if (Object.keys(response.body).length > 0) {
          this.$refs.chart.chart.addSeries({
              name: 'Run ' + index + ', ' + variable,
              id: index + ',' + variable,
              type: 'line',
              animation: {
                duration: this.updateTime
              },
              data: this.responseToData(response, variable)
          })
          this.$refs.chart.chart.reflow();
        }
      })
    },
    addVariable: function(variableName) {
      for (var xp_index of this.selectedExperiments) {
        this.addSeries(xp_index, variableName);
      }
    },
    removeExperiment: function(xp_index) {
      for (var tp of this.toplot) {
        this.$refs.chart.chart.get(xp_index + ',' + tp).remove()
        this.$refs.chart.chart.reflow();
      }
    },
    removeVariable: function(variableName) {
      for (var xp_index of this.selectedExperiments) {
        this.$refs.chart.chart.get(xp_index + ',' + variableName).remove()
        this.$refs.chart.chart.reflow();
      }
    },
    updateSeries: function(xp_index, variableName) {
      this.$http.get('steps/' + xp_index).then(function(response) {
        if (Object.keys(response.body).length > 0) {
          var newData = this.responseToData(response, variableName);
          var oldData = this.$refs.chart.chart.get(xp_index + ',' + variableName).data
          if (newData.length > oldData.length) {
            var newPoints = newData.slice(oldData.length)
            for (var point of newPoints) {
              // maybe here don't redraw all points
              this.$refs.chart.chart.get(xp_index + ',' + variableName).addPoint(point, true);
            }
            this.$refs.chart.chart.reflow();
          }
        }
      })
    },
    runLiveUpdate: function() {
      this.intervalControl = setInterval(() => {
        for (var xp of this.selectedExperiments) {
          for (var varname of this.toplot) {
            this.updateSeries(xp, varname)
          }
        }
        }, 1000);
      this.updateTime = 0;
    },
    stopLiveUpdate: function() {
      clearInterval(this.intervalControl);
      this.updateTime = 200;
    }
  },
  watch: {
    toplot_val: function(newVal, oldVal) {
      if (newVal.length < oldVal.length) {
        if (newVal.length > 0) {
          var to_remove = oldVal.filter(item => { return newVal.indexOf(item) < 0; })
        } else {
          var to_remove = oldVal;
        }
        for (var to_remove_name of to_remove) {
          this.removeVariable(to_remove_name);
        }
      } else if (newVal.length > oldVal.length) {
        var to_add = newVal.filter(item => { return oldVal.indexOf(item) <  0; })
        for (var to_add_name of to_add) {
          this.addVariable(to_add_name);
        } 
      }
    },
    selectedExperiments: {
      handler :function(newVal, oldVal) {
        if (newVal.length < oldVal.length) {
          if (newVal.length > 0) {
            var to_remove = oldVal.filter(item => { return newVal.indexOf(item) < 0; })
          } else {
            var to_remove = oldVal;
          }
          for (var to_remove_index of to_remove) {
            this.removeExperiment(to_remove_index);
          }
        } else if (newVal.length > oldVal.length) {
          var to_add = newVal.filter(item => { return oldVal.indexOf(item) < 0; })
          for (var to_add_index of to_add) {
            this.addExperiment(to_add_index);
          } 
        }
      },
      deep: true 
    },
    liveUpdate: function(newVal, oldVal) {
      newVal ? this.runLiveUpdate() : this.stopLiveUpdate();
    }
  },
  props: ["selectedExperiments", "experiments"]
}
</script>

<style lang="scss">
// .highcharts-container {
//     width:99% !important;
//     height:99% !important;
// }
</style>
