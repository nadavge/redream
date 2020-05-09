import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    dreamcastState: {
      connections: {
        current: [],
        history: []
      }
    }
  },
  mutations: {
    syncDreamcastState(state, dreamcastState) {
      state.dreamcastState = dreamcastState;
    },
    addNewConnection(state, connection) {
      state.dreamcastState.connections.current.push(connection);
    }
  },
  actions: {},
  modules: {}
});
