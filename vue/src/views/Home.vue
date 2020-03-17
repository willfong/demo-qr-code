<template>
  <div class="home">
    <img src="/static/lookup.png" />
    <h1 class="title">Report of Scans</h1>
    <ul>
      <li v-for="l in report" v-bind:key="l.id">{{l.id}}: {{l.count}}</li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "home",
  data() {
    return {
      report: []
    }
  },
  mounted() {
    axios.get("/report", {params: {id: this.id}}).then(response => {
      this.report = response.data;
    });
  }
};
</script>
