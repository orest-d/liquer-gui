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
        <v-list-item link href="#-i-mode/content">
          <v-list-item-icon>
            <v-icon>mdi-eye</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Content</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link href="#-i-mode/store">
          <v-list-item-icon>
            <v-icon>mdi-folder</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Store</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link href="#-i-mode/commands">
          <v-list-item-icon>
            <v-icon>mdi-view-list</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Commands</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link href="#-i-mode/clean">
          <v-list-item-icon>
            <v-icon>mdi-delete</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Clean</v-list-item-title>
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
      <v-menu
        :rounded="rounded"
        open-on-hover
        offset-y
        transition="slide-x-transition"
        bottom
        right
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-bind="attrs" v-on="on"> Services </v-btn>
        </template>
        <v-list dense>
          <v-list-item
            v-for="(item, index) in services"
            :key="index"
            router
            :to="item.link"
          >
            <v-list-item-action>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-spacer></v-spacer>
      <v-menu
        open-on-hover
        offset-y
        transition="slide-x-transition"
        bottom
        right
        v-if="mode == 'store'"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn text v-bind="attrs" v-on="on"> New </v-btn>
        </template>
        <v-list dense>
          <v-list-item href="#-i-mode/new_file">
            <v-list-item-action>
              <v-list-item-title>New file</v-list-item-title>
            </v-list-item-action>
          </v-list-item>
          <v-list-item href="#-i-mode/upload_file">
            <v-list-item-action>
              <v-list-item-title>Upload file</v-list-item-title>
            </v-list-item-action>
          </v-list-item>
          <v-list-item href="#-i-mode/create_folder">
            <v-list-item-action>
              <v-list-item-title>Create folder</v-list-item-title>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-btn v-if="can_edit" href="#-i-mode/edit">Edit</v-btn>
      <v-btn v-if="mode == 'content'" href="#-i-mode/metadata">Metadata</v-btn>
      <v-btn v-if="mode == 'metadata'" href="#-i-mode/content">Content</v-btn>
    </v-app-bar>
    <v-main>
      <!--  -->
      <v-container v-if="mode == 'store'" fluid>
        <v-row>
          <v-col cols="1">
            <v-btn @click="updir()" icon
              ><v-icon>mdi-arrow-up-thin-circle-outline</v-icon></v-btn
            >
            <v-btn @click="sync()" icon>
              <v-icon>mdi-sync</v-icon>
            </v-btn>
          </v-col>
          <v-col cols="10">{{ dirkey }}</v-col>
          <v-col cols="1">
            <v-btn @click="make_dir()" icon>
              <v-icon>mdi-play-box-outline</v-icon>
            </v-btn>
            <v-btn @click="clean_dir()" icon>
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>

      <Clean v-if="mode == 'clean'" @message-event="message_event($event)" />

      <DirView
        v-if="mode == 'store'"
        :dirkey="dirkey"
        :tick="tick"
        @message-event="message_event($event)"
        @open-event="open_event($event)"
      />

      <Content
        v-if="mode == 'content'"
        :metadata="metadata"
        @message-event="message_event($event)"
      />
      <MetadataView
        v-if="mode == 'metadata'"
        :metadata="metadata"
        @message-event="message_event($event)"
      />

      <Commands
        v-if="mode == 'commands'"
        :liquer_url="liquer_url"
        @message-event="message_event($event)"
      />
      <PlainTextStoreEditor
        v-if="show_plain_text_editor"
        :metadata="metadata"
        @message-event="message_event($event)"
      />
      <HighlightingTextStoreEditor
        v-if="show_highlighting_text_editor"
        :metadata="metadata"
        @message-event="message_event($event)"
      />
      <NewFile
        v-if="mode == 'new_file'"
        :dirkey="dirkey"
        @message-event="message_event($event)"
        @open-event="open_event($event)"
      />
      <NewFolder
        v-if="mode == 'create_folder'"
        :dirkey="dirkey"
        @message-event="message_event($event)"
        @open-event="open_event($event)"
      />

    </v-main>
    <StatusBar :status="status" :message="message" />
  </v-app>
</template>

<script>
import StatusBar from "./components/StatusBar";
import Commands from "./components/Commands";
import Content from "./components/Content";
import MetadataView from "./components/MetadataView";
import DirView from "./components/DirView";
import Clean from "./components/Clean";
import PlainTextStoreEditor from "./components/PlainTextStoreEditor";
import HighlightingTextStoreEditor from "./components/HighlightingTextStoreEditor";
import NewFile from "./components/NewFile";
import NewFolder from "./components/NewFolder";

export default {
  name: "App",

  components: {
    StatusBar,
    Commands,
    Content,
    DirView,
    MetadataView,
    Clean,
    PlainTextStoreEditor,
    HighlightingTextStoreEditor,
    NewFile,
    NewFolder,
  },

  data: () => ({
    drawer: false,
    mode: "",
    query: "",
    is_key: false,
    data: null,
    dirkey: "",
    tick: 0,
    metadata: null,
    status: "OK",
    message: "",
    message_event_object: { status: "OK" },
    url_query_prefix: "/liquer/q/",
    url_submit_prefix: "/liquer/submit/",
    url_submit_key_prefix: "/liquer/submit/-R/",
    url_remove_prefix: "/liquer/cache/remove/",
    url_stored_meta_prefix: "/liquer/api/stored_metadata/",


        services: [{
                icon: "mdi-domain",
                title: "Media Monitoring",
                link: "/mmrservices"
            },
            {
                icon: "mdi-message-text",
                title: "Audience Measurement",
                link: "/amrservices"
            },
            {
                icon: "mdi-flag",
                title: "Integration Analysis"
            }
        ],


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
        window.location.href = "#-i-store/" + this.dirkey;
      } else {
        this.mode = "content";
        this.query = "";
        this.key = item.key;
        this.is_key = true;
        window.location.href = "#-i-k/" + this.key;
        //this.submit_query(item.key, true);
      }
    },
    update_route() {
      console.log("Update route", window.location.hash);
      this.route = window.location.hash;
      if (this.route.startsWith("#")) {
        this.route = this.route.substring(1);
      }
      var route_table = {
        mode(self, argument) {
          self.set_mode(argument);
          if (this.mode == "content") {
            if (this.is_key) {
              self.submit_query(this.key, true);
            } else {
              self.submit_query(this.query);
            }
          }
        },
        store(self, argument) {
          self.dirkey = argument;
          self.set_mode("store");
        },
        q(self, argument) {
          self.set_mode("content");
          self.submit_query(argument);
        },
        qm(self, argument) {
          self.set_mode("metadata");
          self.submit_query(argument);
        },
        k(self, argument) {
          self.key = argument;
          self.is_key = true;
          self.set_mode("content");
          self.submit_query(argument, true);
        },
        km(self, argument) {
          self.key = argument;
          self.is_key = true;
          self.set_mode("metadata");
          self.load_stored_metadata("-R/" + argument);
        },
      };
      var recognized = false;
      for (const instruction in route_table) {
        var prefix = "-i-" + instruction + "/";
        console.log("Try prefix", prefix);
        if (this.route.startsWith(prefix)) {
          recognized = true;
          var argument = this.route.substring(prefix.length);
          console.log("  Route instruction", instruction);
          console.log("  Route argument", argument);
          route_table[instruction](this, argument);
          return;
        }
      }
      if (!recognized) {
        //this.error("Route not recognized");
        console.log("Route not recognized");
      }
    },
    set_mode(mode) {
      this.mode = mode;
      this.drawer = false;
    },
    updir() {
      console.log("Updir from", this.dirkey);
      this.dirkey = this.dirkey.split("/").slice(0, -1).join("/");
      console.log("Updir to", this.dirkey);
      window.location.href = "#-i-store/" + this.dirkey;
    },
    clean_dir() {
      console.log("Clean dir", this.dirkey);
      var url = this.url_query_prefix;
      if (this.dirkey == "") {
        url = url + "ns-meta/root_key/clean-t-t-t-t-f/result.json";
      } else {
        url =
          url +
          "-R-meta/" +
          this.dirkey +
          "/-/ns-meta/clean-t-t-t-t-f/result.json";
      }
      console.log("Clean URL", url);
      this.$http.get(url).then(
        function (response) {
          response.json().then(
            function (data) {
              console.log("clean result: ", data);
              this.tick += 1;
            }.bind(this),
            function (reason) {
              this.error("JSON error while cleaning " + this.dirkey, reason);
              this.tick += 1;
            }.bind(this)
          );
        }.bind(this),
        function (reason) {
          this.error("Failed calling clean " + this.dirkey, reason);
        }.bind(this)
      );
    },
    make_dir() {
      console.log("make dir", this.dirkey);
      var url = this.url_query_prefix;
      if (this.dirkey == "") {
        url = url + "ns-meta/root_key/make_recipes-f/result.json";
      } else {
        url =
          url +
          "-R-meta/" +
          this.dirkey +
          "/-/ns-meta/make_recipes-f/result.json";
      }
      console.log("Make dir URL", url);
      this.$http.get(url).then(
        function (response) {
          response.json().then(
            function (data) {
              console.log("Make dir result: ", data);
              this.tick += 1;
            }.bind(this),
            function (reason) {
              this.error("JSON error while make dir " + this.dirkey, reason);
              this.tick += 1;
            }.bind(this)
          );
        }.bind(this),
        function (reason) {
          this.error("Failed calling make_recipes " + this.dirkey, reason);
        }.bind(this)
      );
    },

    load_stored_metadata(query = null, callback = () => {}) {
      if (query == null) {
        query = this.query;
      }
      console.log("Load stored metadata", query);
      this.$http.get(this.url_stored_meta_prefix + query).then(
        function (response) {
          response.json().then(
            function (data) {
              this.metadata = data;
              callback();
            }.bind(this),
            function (reason) {
              this.error(
                "JSON error while loading stored metadata",
                reason,
                query
              );
            }.bind(this)
          );
        }.bind(this),
        function (reason) {
          this.error("Failed loading stored metadata", reason, query);
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
    sync() {
      console.log("Sync");
      var url = this.url_query_prefix + "sync_store/result.json";
      console.log("GET", url);
      this.$http.get(url).then(
        function (response) {
          response.json().then(
            function (data) {
              if (data.status == "OK") {
                this.info(data.message);
              } else {
                this.error(data.message);
              }
              this.tick += 1;
            }.bind(this),
            function (reason) {
              this.error("JSON error while sync", reason);
            }.bind(this)
          );
        }.bind(this),
        function (reason) {
          this.error("Failed to sync", reason);
        }.bind(this)
      );
    },
    monitor_query(query = null, callback = function () {}) {
      if (query == null) {
        query = this.query;
      }
      console.log("Monitor query", query);
      this.load_stored_metadata(
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
            this.info("Data ready", this.metadata, query);
            callback();
          } else if (this.metadata.status == "external") {
            this.info("External data ready", this.metadata, query);
            callback();
          } else if (this.metadata.status == "expired") {
            this.info("Expired data available", this.metadata, query);
            callback();
          } else if (this.metadata.status == "side-effect") {
            this.info(
              "Data ready (created as a side-effect)",
              this.metadata,
              query
            );
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
    submit_query(query, is_key = false) {
      console.log("Submit query", query);
      this.query = query;
      this.is_key = is_key;

      var url = "";
      if (is_key) {
        this.info("Submitting key", {}, query);
        url = this.url_submit_key_prefix + query;
        console.log("Submitting key, url:", url);
      } else {
        this.info("Submitting query", {}, query);
        url = this.url_submit_prefix + query;
        console.log("Submitting query, url:", url);
      }
      this.$http.get(url).then(
        function (response) {
          response.json().then(
            function (data) {
              try {
                if (data.status == "OK") {
                  this.info(data.message, data, query);
                  if (is_key) {
                    query = "-R/" + query;
                  }
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
  computed: {
    can_edit() {
      return this.mode == "content" || this.mode == "metadata";
    },
    show_plain_text_editor() {
      return (
        this.mode == "edit" &&
        typeof this.key == "string" &&
        !this.key.endsWith(".yaml")
      );
    },
    show_highlighting_text_editor() {
      return (
        this.mode == "edit" &&
        typeof this.key == "string" &&
        this.key.endsWith(".yaml")
      );
    },
  },
  created() {
    //    this.mode="content";
    //    this.submit_query("harmonic");
    this.mode = "";
    window.onhashchange = this.update_route;
    this.update_route();
  },
};
</script>
