<template>
  <v-simple-table dense>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left" style="max-width:32px">
          </th>
          <th class="text-left">
            Name
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="item in dir_status" :key="item.key"
        >
          <td style="max-width:32px"><v-icon v-text="icon(item)"></v-icon></td>
          <td><v-btn v-text="item.name" @click="open_item(item)"></v-btn></td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
export default {
  props: {
    liquer_url: {
      type: String,
      default: "/liquer",
    },
    dirkey: {
      type: String,
      default: "",
    },
  },
  data: () => ({
    url_query_prefix: "/liquer/q/",
    url_submit_prefix: "/liquer/submit/",
    dir_status: [],
  }),
  methods: {
    info(message, reason = null, query = null) {
      this.message_event({ status: "INFO", message, reason, query });
    },
    error(message, reason = null, query = null) {
      this.message_event({ status: "ERROR", message, reason, query });
    },
    message_event(m) {
      this.$emit("message-event", m);
    },
    icon(item) {
      if (item.is_dir) {
        return "mdi-folder";
      } else {
        return "mdi-file";
      }
    },
    open_item(item) {
      this.$emit("open-event", item);
    },
    fetch_dir_status(key) {
      this.info("Fetching dir info " + key);
      var query = "";
      if (key == "") {
        query = this.url_query_prefix + "ns-meta/dir_status/status.json";
      } else {
        query =
          this.url_query_prefix +
          "-R-meta/" +
          key +
          "/-/ns-meta/dir_status/status.json";
      }
      console.log("Fetching dir info from query", query);
      this.dir_status = [];
      this.$http.get(query).then(
        function (response) {
          response.json().then(
            function (data) {
              if (data.status == "OK") {
                this.dir_status = data.data;
              } else {
                this.error(data.message);
              }
            }.bind(this),
            function (reason) {
              this.error("JSON error while fetching dir info", reason, query);
            }.bind(this)
          );
        }.bind(this),
        function (reason) {
          this.error("Failed loading dir info", reason, query);
        }.bind(this)
      );
    },
  },
  watch: {
    dirkey(new_dirkey, old_dirkey) {
      if (new_dirkey != old_dirkey) {
        this.fetch_dir_status(new_dirkey);
      }
    },
  },
  created() {
    this.fetch_dir_status(this.dirkey);
  },
};
</script>