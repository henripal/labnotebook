<template>
<div id="app">
  <v-app id="inspire">
    <v-navigation-drawer
    clipped
    v-model='drawer'
    fixed
    app>
    <v-list>
      <br>
      <v-list-tile>
          <v-select
            :items="Object.keys(experiments).filter(x => !selectedExperiments.includes(x)).sort((a, b)=> (b-a))"
            v-model="selectedExperiment"
            label="Add Experiment" min-width="300px" class="pr-5">
          </v-select>
          <v-btn flat icon>
            <v-icon @click="getExperiments()">cached</v-icon>
          </v-btn>
      </v-list-tile>
      <transition-group name="list-complete" tag="div">
        <v-list-tile v-for="(element, i) in selectedExperiments" @click="" avatar class="list-complete-item" :key="element">
            <v-list-tile-avatar>
              <v-icon small>fas fa-calculator</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title >Run no. {{element}}</v-list-tile-title>
              <v-tooltip bottom>
                <v-list-tile-sub-title slot="activator">Date: {{experiments[element].dt}}</v-list-tile-sub-title>
                <span>{{ experiments[element].model_desc }}</span>
              </v-tooltip>
            </v-list-tile-content>
          <v-list-tile-action right>
            <v-btn icon ripple @click="removeExperiment(i)">
              <v-icon color="grey lighten-1">close</v-icon>
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </transition-group>
    </v-list>

    </v-navigation-drawer>
    <v-toolbar color="primary" dark fixed app clipped-left>
      <v-toolbar-side-icon @click.stop="drawer =! drawer"></v-toolbar-side-icon>
      
      <v-toolbar-title><v-icon medium left>fas fa-flask</v-icon>Lab Notebook   </v-toolbar-title>
    </v-toolbar>
    <v-content>
      <v-container grid-list-xl text-xs-center fluid>
        <v-layout row wrap>
          <v-flex xs6>
            <app-chart-card :selectedExperiments="selectedExperiments" :experiments="experiments"></app-chart-card>
          </v-flex>

          <v-flex xs6>
            <app-chart-card :selectedExperiments="selectedExperiments" :experiments="experiments"></app-chart-card>
          </v-flex>

          <v-flex xs6>
            <v-data-table :items="flatExperiments" :headers="headers" class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-right">{{ props.item.run_id }}</td>
                <td class="text-xs-right">{{ props.item.dt }}</td>
                <td class="text-xs-right">{{ props.item.gpu }}</td>
                <td class="text-xs-right">{{ Math.round(100*props.item.final_valacc)/100 }}</td>
                <td class="text-xs-right">{{ Math.round(100*props.item.final_trainacc)/100 }}</td>
                <td class="text-xs-right">{{ Math.round(100*props.item.final_trainloss)/100 }}</td>
              </template>
            </v-data-table>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</div>
</template>

<script>
import chartCard from './components/chartCard.vue'

export default {
  data () {
    return {
      drawer: true,
      experiments: [],
      selectedExperiments: [],
      selectedExperiment: '',
      items: [],
      headers: [
        {text: 'Run Id', value: 'run_id', align: 'right'},
        {text: 'Date Time', value: 'dt', align: 'right'},
        {text: 'GPU ID', value: 'gpu', align: 'right'},
        {text: 'Val. Acc.', value: 'final_valacc', align: 'right'},
        {text: 'Train. Acc.', value: 'final_trainacc', align: 'right'},
        {text: 'Train. Loss', value: 'final_trainloss', align: 'right'}
      ]
    }
  },
  components: {
    appChartCard: chartCard
  },
  computed: {
    flatExperiments() {
      var result = [];
      for (var experiment_key of Object.keys(this.experiments)) {
        result.push(this.experiments[experiment_key])
      }
      return result;
    }
  },
  watch: {
    selectedExperiment: function(newval, oldval)  {
      this.addExperiment(newval);
    }
  },
  methods: {
    getExperiments() {
      this.$http.get('experiments').then(response => {
        var dict = {}
        for (var experiment of response.body) {
          dict[experiment.run_id] = experiment
        }
        this.experiments =  dict ;
      })
    },
    removeExperiment: function(index_toremove) {
      // do this swap rather than mutate
      // so we can watch for changes
      let newSelected = this.selectedExperiments.slice(0);
      newSelected.splice(index_toremove,1);
      this.selectedExperiments = newSelected;
    },
    addExperiment: function(index_toadd) {
      // do this swap rather than mutate
      // so we can watch for changes
      let newSelected = this.selectedExperiments.slice(0);
      newSelected.push(index_toadd);
      this.selectedExperiments = newSelected;
    }
  },
  beforeMount() {
    this.getExperiments()
  }
}
</script>

<style>
.list-complete-item {
  transition: all 500ms;
  display: inline-block;
}
.list-complete-enter, .list-complete-leave-to
/* .list-complete-leave-active below version 2.1.8 */ {
  opacity: 0;
  transform: translateY(-30px);
}
.list-complete-leave-active {
  position: absolute;
}

</style>
