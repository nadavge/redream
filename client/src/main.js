import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import io from "socket.io-client";

let socket = io("http://localhost:8000");

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App),
  created() {

    socket.on("connect", () => {
      console.log("connection established");
    });

    socket.on("sync_state", (data) => {
      this.$store.commit('syncDreamcastState', data);
      console.log("SYNC:" + data);
    });

    socket.on("new_connection", (data) => {
      this.$store.commit('addNewConnection', data);
      console.log("NEW_CONNECTION:" + [data]);
    });

  }
}).$mount("#app");
