<template>
  <v-data-table :headers="headers" :items="dir_status" class="elevation-1">
    <template v-slot:item.icon="{ item }">
      <v-icon v-text="item.icon" />
    </template>
    <template v-slot:item.status="{ item }">
      <ResultStatus v-if="!item.is_dir" :status="item.status" />
    </template>
    <template v-slot:item.name="{ item }">
      <span @click="open_item(item)">{{ item.name }}</span>
    </template>
    <template v-slot:item.control="{ item }">
        <v-btn v-if="can_rerun(item)" @click="remove_key(item.key)">
            <v-icon>mdi-autorenew</v-icon>
        </v-btn>
    </template>
  </v-data-table>
</template>

<script>
import ResultStatus from "./ResultStatus";

export default {
  components: {
    ResultStatus,
  },

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
    url_remove_prefix: "/liquer/api/store/remove/",
    dir_status: [],
    headers: [
      {
        text: "",
        align: "start",
        sortable: true,
        value: "icon",
        width: "32px",
      },
      { text: "Status", value: "status", width: "50px" },
      { text: "Name", value: "name" },
      { text: "Characteristics", value: "data_characteristics" },
      { text: "Message", value: "message" },
      { text: "Title", value: "title" },
      { text: "Updated", value: "updated" },
      { text: "Size", value: "size" },
      { text: "", value:"control", sortable: false,}
    ],
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
    can_rerun(item) {
        return item.has_recipe && item.status=="ready";
    },
    open_item(item) {
      this.$emit("open-event", item);
    },
    updir() {
      this.open_item({
          key: this.dirkey.split("/").slice(0, -1).join("/"),
          is_dir: true
      });
    },
    remove_key(key){
      this.info("Remove " + key);
      var query = "";
      if (key == "") {
          console.log("Attempt to remove", key);
          return;
      } else {
        query = this.url_remove_prefix + key;
      }
      console.log("Remove query", query);
      this.$http.get(query).then(
        function (response) {
          response.json().then(
            function (data) {
              if (data.status == "OK") {
                this.info("Removed "+key);
                this.fetch_dir_status(this.dirkey);
              } else {
                this.error(data.message);
                this.fetch_dir_status(this.dirkey);
              }
            }.bind(this),
            function (reason) {
              this.error("JSON error while removing "+key, reason, query);
              this.fetch_dir_status(this.dirkey);
            }.bind(this)
          );
        }.bind(this),
        function (reason) {
          this.error("Failed to remove "+key, reason, query);
          this.fetch_dir_status(this.dirkey);
        }.bind(this)
      );
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
                for (var i = 0; i < this.dir_status.length; i++) {
                  this.dir_status[i].icon = this.icon(this.dir_status[i]);
                }
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