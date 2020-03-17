<template>
  <div class="lookup">
    <h1>Your Id: {{id}}</h1>
    <h1>I have seen you: {{count}} times</h1>
    <h2>Some things I know about you: {{location}}</h2>
    <button class="button is-success" @click="$router.push('/')">Go back</button>
    <button class="button is-danger" @click="resetToken">Change Token</button>
  </div>
</template>

<script>
import axios from "axios";

function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

export default {
  name: "lookup",
  data() {
    return {
      id: false,
      count: 0,
      location: {},
    }
  },
  mounted() {
    if (!localStorage.id) {
      localStorage.id = uuidv4();
    }
    this.id = localStorage.id;
    axios.get("/lookup", {params: {id: this.id}}).then(response => {
      this.count = response.data.count;
      this.location = response.data.location;
      //console.log(response.data); // eslint-disable-line no-console
    });
  },
  methods: {
    resetToken() {
      localStorage.id = uuidv4();
      this.id = localStorage.id;
      axios.get("/lookup", {params: {id: this.id}}).then(response => {
        this.count = response.data.count;
        this.location = response.data.location;
        //console.log(response.data); // eslint-disable-line no-console
      });
    }
  }
};
</script>
