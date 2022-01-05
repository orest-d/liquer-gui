<template>
  <v-container class="fill-height" fluid>
    <v-row v-if="mode == 'none' || mode == 'waiting'">
      <v-col cols="8">
        <h4 v-if="mode == 'none'">No metadata</h4>
        <h4 v-if="mode == 'waiting'">Waiting for {{ metadata.query }}</h4>
      </v-col>
      <v-col cols="4">
        <v-progress-circular
          :size="50"
          :width="10"
          color="primary"
          indeterminate
        ></v-progress-circular>
      </v-col>
    </v-row>
    <v-row v-if="mode == 'none'">
      <v-col>
        <MetadataView
          :metadata="metadata"
          @message-event="message_event($event)"
        />
      </v-col>
    </v-row>
    <v-row v-if="mode == 'recipe'">
      <v-col>
        <MetadataView
          :metadata="metadata"
          @message-event="message_event($event)"
        />
      </v-col>
    </v-row>
    <v-row v-if="mode == 'waiting'">
      <v-col>
        <MetadataView
          :metadata="metadata"
          @message-event="message_event($event)"
        />
      </v-col>
    </v-row>
    <v-row v-if="mode == 'error'">
      <v-col>
        Query {{ metadata.query }} failed.
        <p>{{ metadata.message }}</p>
        <MetadataView
          :metadata="metadata"
          @message-event="message_event($event)"
        />
      </v-col>
    </v-row>
    <v-row v-if="mode == 'invalid'">
      <v-col> Invalid metadata </v-col>
    </v-row>
    <div v-if="mode == 'text'">
      <pre>{{ data }}</pre>
    </div>
    <div v-if="mode == 'link'">
    <h3>{{ title }}</h3>
    <em>{{ data_description }}</em>
    <br />
    <pre>{{ description }}</pre>
      Content: <a :href="external_link"><v-icon>mdi-link</v-icon>{{external_link_description}}</a>
    </div>
    <div v-if="mode == 'iframe'" style="width:100%; height:100%;">
      <iframe
        width="100%"
        height="100%"
        :src="external_link"
        frameBorder="0"
        style="background-color: white;"        
      ></iframe>
    </div>
    <div v-if="mode == 'image'">
        <img :src="external_link" aspect-ratio="1" style="width:100%; height:100%;object-fit: scale-down;"/>
    </div>
    <v-layout row wrap v-if="mode == 'dataframe'">
      <v-flex
        >Pandas version: {{ data.schema.pandas_version }}
        <v-btn :href="pcv_query">PointCloud Viewer</v-btn>
      </v-flex>
      <v-flex xs12 v-if="data != null">
        <v-data-table
          :headers="dataframe_headers"
          :items="dataframe_rows"
          class="elevation-1"
        >
        </v-data-table>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import MetadataView from "./MetadataView";

export default {
  components: {
    MetadataView,
  },
  props: {
    liquer_url: {
      type: String,
      default: "/liquer",
    },
    data: {
      default: null,
    },
    metadata: {
      default: null,
    },
  },
  data: () => ({
    mode: "none",
    data_ready: false,
    url_query_prefix: "/liquer/q/",
    url_store_data_prefix: "/liquer/api/store/data/",
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
    update() {
      if (this.metadata == null) {
        this.mode = "none";
      }
      if (this.metadata.status == null) {
        this.mode = "invalid";
      }
      if (this.metadata.status == "error") {
        this.mode = "error";
      }
      if (this.metadata.status == "recipe") {
        this.mode = "recipe";
      }
      if (
        this.metadata.status == "evaluation" ||
        this.metadata.status == "parent" ||
        this.metadata.status == "dependencies" ||
        this.metadata.status == "submitted"
      ) {
        this.mode = "waiting";
      }
      if (
        this.metadata.status == "ready" ||
        this.metadata.status == "external" ||
        this.metadata.status == "expired" ||
        this.metadata.status == "side-effect"
      ) {
        console.log("READY");
        console.log("Query", this.metadata.query);
        console.log("Type", this.metadata.type_identifier);
        console.log("Metadata", this.metadata);
        var type_actions = {
          generic() {
            this.just_load("text");
          },
          text() {
            if (this.metadata.mimetype == "text/html") {
              this.mode = "iframe";
            } else if (this.metadata.mimetype.startsWith("image/")) {
              this.mode = "image";
            } else {
              this.just_load("text");
            }
          },
          dataframe() {
            this.just_load_json(
              "dataframe",
              this.metadata.query + "/head_df-1000/data.json"
            ); // FIXME: Handle filename
          },
          matplotlibfigure() {
            this.mode = "image";
          },
        };
        try {
          type_actions[this.metadata.type_identifier].bind(this)();
        } catch (e) {
          if (this.metadata.mimetype.startsWith("text/")) {
            this.mode = "iframe";
          } else if (this.metadata.mimetype.startsWith("image/")) {
            this.mode = "image";
          } else {
            if (!(this.metadata.type_identifier in type_actions)) {
              this.info(
                "Undefined data type: " + this.metadata.type_identifier
              );
              this.mode="link";
            } else {
              this.error("Error dispatching content");
            }
            console.log(e.stack);
          }
        }
      }
      return "waiting";
    },
    just_load(mode, query = null) {
      if (query == null) {
        query = this.metadata.query;
      }
      if (query == null) {
        query = "-R/" + this.metadata.key;
      }
      console.log("Just load", query);
      this.$http.get(this.url_query_prefix + query).then(
        function (response) {
          this.data = response.body;
          this.mode = mode;
        }.bind(this),
        function (reason) {
          this.error("Failed loading data", reason, query);
        }.bind(this)
      );
    },
    just_load_json(mode, query = null) {
      if (query == null) {
        query = this.metadata.query;
      }
      if (query == null) {
        query = "-R/" + this.metadata.key;
      }
      console.log("Just load JSON", query);
      this.$http.get(this.url_query_prefix + query).then(
        function (response) {
          response.json().then(
            function (data) {
              this.data = data;
              this.info("Data loaded.");
              console.log("Mode:", mode);
              this.mode = mode;
            }.bind(this),
            function (reason) {
              this.error("Json error (data)", reason);
            }.bind(this)
          );
        }.bind(this),
        function (reason) {
          this.error("Failed loading data", reason, query);
        }.bind(this)
      );
    },
  },
  watch: {
    metadata() {
      console.log("Metadata updated in content");
      this.update();
    },
  },
  created() {
    console.log("Content created");
    this.update();
  },
  computed: {
    title() {
      try {
        return this.metadata.title;
      } catch {
        return "";
      }
    },
    description() {
      try {
        return this.metadata.description;
      } catch {
        return "";
      }
    },
    key() {
      try {
        return this.metadata.key;
      } catch {
        return "";
      }
    },
    data_description() {
      try {
        return this.metadata.data_characteristics.description;
      } catch {
        return "";
      }
    },
    pcv_query() {
      if (typeof this.metadata.key == "string") {
        return "#-i-q/-R/" + this.metadata.key + "/-/dr/pointcloud-viewer.html";
        //return this.url_query_prefix + "-R/"+this.metadata.key+"/-/dr/pointcloud-viewer.html";
      } else {
        return "#-i-q/" + this.metadata.query + "/pointcloud-viewer.html";
        //return this.url_query_prefix +this.metadata.query +"/pointcloud-viewer.html";
      }
    },
    external_link() {
      if (typeof this.metadata.key == "string") {
        return this.url_store_data_prefix + this.metadata.key;
      } else {
        return this.url_query_prefix + this.metadata.query;
      }
    },
    external_link_description() {
      if (typeof this.metadata.key == "string") {
        return this.metadata.key+" (key)";
      } else {
        return this.metadata.query+" (query)";
      }
    },
    dataframe_headers: function () {
      if (this.data == null) {
        return [];
      } else {
        var h = [];

        this.data.schema.fields.forEach(function (x) {
          h.push({
            text: x.name,
            value: x.name,
          });
        });
        console.log(h);
        return h;
      }
    },
    dataframe_rows: function () {
      if (this.data == null) {
        return [];
      } else {
        console.log("rows", this.data.data);
        return this.data.data;
      }
    },
  },
};
</script>