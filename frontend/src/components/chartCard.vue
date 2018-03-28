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
            <v-checkbox label='Val. Acc.' v-model="standardFields" value="valacc"></v-checkbox>
          </v-list-tile>
          <v-list-tile>
            <v-checkbox label='Train. Acc.' v-model="standardFields" value="trainacc"></v-checkbox>
          </v-list-tile>
          <v-list-tile>
            <v-checkbox label='Train. Loss' v-model="standardFields" value="trainloss"></v-checkbox>
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
          <v-list-tile>
            <v-list-tile-content>
              <v-list-tile-title>
              Custom variables:
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile v-for="field in this.possibleCustomFieldsList" :key="field">
            <v-checkbox :label="field" v-model="customFields" :value="field"></v-checkbox>
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
      lastUpdate: {},
      possibleStandardFields: ['trainacc', 'valacc', 'trainloss'],
      possibleCustomFields:  {},
      possibleCustomFieldsList:  [],
      customFields: [],
      intervalControl: null,
      standardFields: ['trainacc'],
      selectitems: ['line', 'bar'],
      options: {
        chart: {
          zoomType: 'x'
        },
        yAxis: {
          title: {text: 'trainacc' },
          type: 'linear'
        },
        xAxis: {
          title: {text: 'timestep'}
        },
        title: null,
        series: [{id: 'dummy', data: [null, null]}]
      }
    }
  },
  computed: {
    computedStandardFields: function() {
      return this.standardFields;
    },
    computedAllFields: function() {
      return this.standardFields.concat(this.customFields)
    }
  },
  methods: {
    updatePossibleCustomFields: function() {
      //this.possibleCustomFields = {}
      for (var experiment of this.selectedExperiments) {
        this.getCustomFields(experiment);
      }
    },
    updatePossibleCustomFieldList: function() {
      this.possibleCustomFieldsList = Array.from(new Set([].concat.apply([], Object.values(this.possibleCustomFields))))
    },
    getCustomFields: function(experiment_id) {
      this.$http.get('customfieldnames/' + experiment_id).then(function(response) {
        this.possibleCustomFields[experiment_id] = response.body
        this.updatePossibleCustomFieldList()
      })
    }, 
    responseToData: function(response, seriesname) {
      var localname = this.possibleStandardFields.includes(seriesname) ? seriesname : 'cf'
      var y = response.body[localname]
      var x = response.body.timestep

      return x.map((e, i) => { return [e, y[i]]})
    },
    addExperiment: function(experiment_id) {
      for (var tp of this.computedAllFields) {
        this.addSeries(experiment_id, tp)
      }
    },
    addSeries: function(index, variable) {
      var dummy = this.$refs.chart.chart.get('dummy');
      if (dummy !== undefined) { dummy.remove(); }

      if (this.possibleStandardFields.includes(variable)) {
        var url = 'steps/' + index
      } else {
        var url = 'customfields/' + index + '?fieldname=' + variable
      }

      this.$http.get(url).then(function(response) {
        if (Object.keys(response.body).length > 0) {
          var ha = this.$refs.chart.chart.addSeries({
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
      var localCustomFields = []
      for (var cf of this.customFields) {
        if (this.possibleCustomFields[xp_index].includes(cf)) {
          localCustomFields.push(cf)
        }
      }
      var newFieldList = this.standardFields.concat(localCustomFields)

      for (var tp of newFieldList) {
        this.$refs.chart.chart.get(xp_index + ',' + tp).remove()
        this.$refs.chart.chart.reflow();
      }
    },
    removeVariable: function(variableName) {
      if (this.customFields.includes(variableName)) {
        var xplist = []
        for (var xp_index of this.selectedExperiments) {
          if (this.possibleCustomFields[xp_index].includes(variableName)) {
            xplist.push(xp_index)
          }
        }
      } else {
        var xplist = this.selectedExperiments
      }
      for (var xp_index of xplist) {
        this.$refs.chart.chart.get(xp_index + ',' + variableName).remove()
        this.$refs.chart.chart.reflow();
      }
    },
    updateSeries: function(xp_index, variableName) {
      var last_timestep = this.lastUpdate[xp_index]

      if (this.possibleStandardFields.includes(variableName)) {
        var url = 'steps/' + xp_index
        if (last_timestep) { url = url + '?start_timestep=' + last_timestep}
      } else {
        var url = 'customfields/' + xp_index + '?fieldname=' + variableName
        if (last_timestep) { url = url + '&start_timestep=' + last_timestep}
      }
      this.$http.get(url).then(function(response) {
        if (Object.keys(response.body).length > 0) {
          // store last timestep
          this.lastUpdate['xp_index'] = response.body.timestep[response.body.timestep.length-1]

          var newData = this.responseToData(response, variableName);
          // var oldData = this.$refs.chart.chart.get(xp_index + ',' + variableName).data
          // if (newData.length > oldData.length) {
            // var newPoints = newData.slice(oldData.length)
          var i = 0
          for (var point of newData) {
            // maybe here don't redraw all points
            var redraw = i == newData.length - 1
            i += 1
            this.$refs.chart.chart.get(xp_index + ',' + variableName).addPoint(point, redraw);
          }
          if (newData) { this.$refs.chart.chart.reflow(); }
        }
      })
    },
    runLiveUpdate: function() {
      this.intervalControl = setInterval(() => {
        for (var xp of this.selectedExperiments) {
          for (var varname of this.computedAllFields) {
            this.updateSeries(xp, varname)
          }
        }
        }, 3000);
    },
    stopLiveUpdate: function() {
      clearInterval(this.intervalControl);
    }
  },
  watch: {
    computedAllFields: function(newVal, oldVal) {
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
      this.$refs.chart.chart.yAxis[0].setTitle({ text: newVal})
      // this.options.yAxis.title.text = newVal;
    },
    selectedExperiments: {
      handler :function(newVal, oldVal) {
        this.updatePossibleCustomFields();

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
