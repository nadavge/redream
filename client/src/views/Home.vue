<template>
  <div id="container" style="height:200px; overflow-y: scroll; border:2px #aaa solid;">
    <div v-if="currentConnections.length === 0">No connections yet</div>
    <table v-else id="connections" style="width:200px">
      <tr v-for="connection in $store.state.dreamcastState.connections.current" :key="connection.src_ip + connection.src_port">
        <td>{{ connection.src_ip }}</td>
        <td>{{ connection.src_port }}</td>
        <td>{{ connection.dst_ip  }}</td>
        <td>{{ connection.dst_port  }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "Home",
  computed: {
    currentConnections() {
      return this.$store.state.dreamcastState.connections.current
    }
  }
  // watch: {
  //   connections: function() {
  //     let container = document.getElementById("container")
  //     let connectionList = document.getElementById("connections")
  //     let shouldScroll = Math.abs(container.scrollHeight - (container.scrollTop + container.clientHeight)) < 5

  //     if (shouldScroll) {
  //       container.scrollTo(0, container.scrollHeight - container.clientHeight)
  //     }
  //   }
  // }
};

</script>
