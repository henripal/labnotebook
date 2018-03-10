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
        <v-text-field
        name="input1"
        label="Start Step"
        id="testing"
        type="number"
        v-model="datastart"></v-text-field>
      </v-list-tile>
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
            <app-chart-card :datastart="datastart"></app-chart-card>
          </v-flex>

          <v-flex xs6>
            <app-chart-card :datastart="datastart"></app-chart-card>
          </v-flex>
          <v-flex xs6>
            <v-data-table :items="items" :headers="headers" class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-right">{{ props.item.x }}</td>
                <td class="text-xs-right">{{ props.item.y }}</td>
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
      msg: 'Welcome to Your Vue.js App',
      myResponse: '',
      title: 'proto app',
      datastart: 0,
      items: [],
      headers: [
        {text: 'x', value: 'x', align: 'right'},
        {text: 'y', value: 'y', align: 'right'}
      ]
    }
  },
  components: {
    appChartCard: chartCard
  },
  methods: {
    getData(datastart) {
      this.$http.get('').then(response => {
        this.items =   response.body[0].slice(this.datastart)
      })
    }
  },
  beforeMount() {
    this.getData()
  }
}
</script>

<style lang="scss">
</style>
