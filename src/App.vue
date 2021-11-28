<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list-item @click="drawer = !drawer">
        <v-list-item-content>
          <v-list-item-title class="text-h6"> LiQuer </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item link @click="mode = 'content'">
          <v-list-item-icon>
            <v-icon>mdi-eye</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Content</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link @click="mode = 'store'">
          <v-list-item-icon>
            <v-icon>mdi-folder</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Store</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link @click="mode = 'commands'">
          <v-list-item-icon>
            <v-icon>mdi-view-list</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Commands</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item link href="https://github.com/orest-d/liquer">
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title> LiQuer Home </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app dense>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>LiQuer</v-toolbar-title>
    </v-app-bar>
    <v-main>
      <!--  -->

      <v-btn v-if="mode == 'store'" @click="updir()">Up</v-btn>
      <DirView
        v-if="mode == 'store'"
        :dirkey="dirkey"
        @message-event="message_event($event)"
        @open-event="open_event($event)"
      />

      <Content
        v-if="mode == 'content'"
        :metadata="metadata"
        @message-event="message_event($event)"
      />

      <Commands
        v-if="mode == 'commands'"
        :liquer_url="liquer_url"
        @message-event="message_event($event)"
      />
    </v-main>
    <StatusBar :status="status" :message="message" />
  </v-app>
</template>

<script>
import StatusBar from "./components/StatusBar";
import Commands from "./components/Commands";
import Content from "./components/Content";
import DirView from "./components/DirView";

export default {
  name: "App",

  components: {
    StatusBar,
    Commands,
    Content,
    DirView,
  },

  data: () => ({
    drawer: false,
    mode: "",
    query: "",
    data: null,
    dirkey: "",
    metadata: null,
    status: "OK",
    message: "",
    message_event_object: { status: "OK" },
    url_query_prefix: "/liquer/q/",
    url_submit_prefix: "/liquer/submit/",
    url_remove_prefix: "/liquer/cache/remove/",
    url_cache_meta_prefix: "/liquer/cache/meta/",

    liquer_url: "/liquer",
    html: "",
  }),
  methods: {
    info(message, reason = null, query = null) {
      this.message_event({ status: "INFO", message, reason, query });
    },
    error(message, reason = null, query = null) {
      this.message_event({ status: "ERROR", message, reason, query });
    },
    message_event(m) {
      console.log(`*** ${m.status}:`, m.message);
      if (m.reason != null) {
        console.log("   Reason: ", m.reason);
      }
      if (m.query != null) {
        console.log("   Query:  ", m.query);
      }
      this.message = m.message;
      this.status = m.status;
      this.message_event_object = m;
    },
    open_event(item) {
      console.log("Open", item);
      if (item.is_dir) {
        this.dirkey = item.key;
      }
      else{
        this.mode="content";
        this.submit_query(item.key+"/-/dr");
      }
    },
    updir() {
      console.log("Updir from", this.dirkey);
      this.dirkey = this.dirkey.split("/").slice(0, -1).join("/");
      console.log("Updir to", this.dirkey);
      this.fetch_dir_status(this.dirkey);
    },

    load_cache_metadata(query = null, callback = () => {}) {
      if (query == null) {
        query = this.query;
      }
      console.log("Load cache metadata", query);
      this.$http.get(this.url_cache_meta_prefix + query).then(
        function (response) {
          response.json().then(
            function (data) {
              this.metadata = data;
              callback();
            }.bind(this),
            function (reason) {
              this.error(
                "JSON error while loading metadata from cache",
                reason,
                query
              );
            }.bind(this)
          );
        }.bind(this),
        function (reason) {
          this.error("Failed loading metadata from cache", reason, query);
        }.bind(this)
      );
    },
    get_metadata(query = null, callback = () => {}) {
      if (query == null) {
        query = this.query;
      }
      console.log("Get metadata", query);
      var url =
        this.url_query_prefix +
        this.query_basis(query) +
        "/state/metadata.json";
      console.log("GET", url);
      this.$http.get(url).then(
        function (response) {
          response.json().then(
            function (data) {
              this.metadata = data;
              callback();
            }.bind(this),
            function (reason) {
              this.error("JSON error while loading metadata", reason, query);
            }.bind(this)
          );
        }.bind(this),
        function (reason) {
          this.error("Failed loading metadata", reason, query);
        }.bind(this)
      );
    },
    monitor_query(query = null, callback = function () {}) {
      if (query == null) {
        query = this.query;
      }
      console.log("Monitor query", query);
      this.load_cache_metadata(
        query,
        function () {
          if (this.metadata == null) {
            console.log(`No metadata for ${query}, assuming volatile`);
            this.info("Volatile query", this.metadata, query);
            this.get_metadata(query, callback);
          } else if (this.metadata.status == "error") {
            console.log("Status", this.metadata.status);
            this.error("Query failed", this.metadata, query);
          } else if (this.metadata.status == "ready") {
            this.info("Data is ready", this.metadata, query);
            callback();
          } else {
            console.log("Status", this.metadata.status);
            console.log(`Refresh metadata ${query}`);
            this.info(`Status: ${this.metadata.status}`, this.metadata, query);
            window.setTimeout(this.monitor_query, 500, query, callback);
          }
        }.bind(this)
      );
    },
    submit_query(query) {
      console.log("Submit query", query);
      this.query = query;
      this.info("Submitting query", {}, query);
      this.$http.get(this.url_submit_prefix + query).then(
        function (response) {
          response.json().then(
            function (data) {
              try {
                if (data.status == "OK") {
                  this.info(data.message, data, query);
                  this.monitor_query(
                    query,
                    function () {
                      console.log("Metadata obtained for query", query);
                      console.log("metadata:", this.metadata);
                    }.bind(this)
                  );
                } else {
                  this.error(data.message, data, query);
                }
              } catch (e) {
                this.error(
                  "Unexpected result from query submission",
                  data,
                  query
                );
              }
            }.bind(this),
            function (reason) {
              this.error("JSON error while submitting query", reason, query);
            }.bind(this)
          );
        }.bind(this),
        function (reason) {
          this.error("Failed sumbitting query", reason, query);
        }.bind(this)
      );
    },
    split_query(query) {
      var query_basis = query;
      var q = this.query.split("/").filter(function (x) {
        return x.length;
      });
      var filename = "data";
      var extension = "pickle";
      if (q.length > 0) {
        var last = q[q.length - 1];
        filename = last.replace("-", "_");
        var v = filename.split(".");
        filename = v[0];
        extension = v[v.length - 1];
        if (last.indexOf("-") == -1 && last.indexOf(".") != -1) {
          query_basis = q.slice(0, q.length - 1).join("/");
        }
      }
      return [query_basis, filename, extension];
    },
    query_basis(query) {
      var query_basis = query;
      var q = this.query.split("/").filter(function (x) {
        return x.length;
      });
      if (q.length > 0) {
        var last = q[q.length - 1];
        if (last.indexOf("-") == -1 && last.indexOf(".") != -1) {
          query_basis = q.slice(0, q.length - 1).join("/");
        }
      }
      return query_basis;
    },
  },
  computed: {},
  created() {
    this.mode="content";
    this.submit_query("hello");
  },
};
</script>
