<template>
  <v-container class="fill-height" fluid>
    <v-row v-if="mode != 'text'">
      <v-col cols="8">
        <h4 v-if="mode == 'none'">No metadata</h4>
        <h4 v-if="mode == 'waiting'">Waiting for {{ metadata.query }}</h4>
        <h4 v-if="mode == 'invalid'">Invalid status</h4>
        <h4 v-if="mode == 'error'">Error in {{ metadata.query }}</h4>
        <h4 v-if="mode == 'recipe'">Recipe</h4>
        <h4 v-if="mode == 'unsupported'">Unsupported data type</h4>
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
    <v-row v-if="mode == 'text'">
      <v-col>
        <prism-editor
          class="highlighting-editor"
          v-model="data"
          :highlight="highlighter"
          :line-numbers="lineNumbers"
        ></prism-editor>
      </v-col>
    </v-row>
    <v-row v-if="mode == 'text'">
      <v-col>
        <v-btn @click="save()">Save</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { PrismEditor } from "vue-prism-editor";
import "vue-prism-editor/dist/prismeditor.min.css"; // import the styles somewhere

// import highlighting library (you can use any library you want just return html string)
import { highlight, languages } from "prismjs/components/prism-core";
//import { loadLanguages } from "prismjs/components";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-yaml";
import "prismjs/components/prism-javascript";
import "prismjs/components/prism-python";
import "prismjs/themes/prism-tomorrow.css"; // import syntax highlighting styles

export default {
  components: {
    PrismEditor,
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
    data: "",
    lineNumbers:true,
    language:"yaml",
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
    highlighter(code) {
      return highlight(code, languages[this.language]); //returns html
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
            this.load("text");
          },
          text() {
            this.load("text");
          },
        };
        try {
          type_actions[this.metadata.type_identifier].bind(this)();
        } catch (e) {
          this.mode = "unsupported";
        }
      }
      return "waiting";
    },
    load(mode, key = null) {
      if (key == null) {
        key = this.metadata.key;
      }

      var url = this.url_store_data_prefix + key;
      console.log("Load", key);
      console.log("URL", url);
      this.$http.get(url).then(
        function (response) {
          this.data = response.body;
          this.mode = mode;
        }.bind(this),
        function (reason) {
          this.error("Failed loading data", reason, key);
        }.bind(this)
      );
    },
    save(key = null) {
      console.log("Save");
      if (key == null) {
        key = this.metadata.key;
      }

      var url = this.url_store_data_prefix + key;
      console.log("Save", key);
      console.log("URL", url);
      this.$http.post(url, this.data).then(
        function (response) {
          response.json().then(
            function (data) {
              console.log("save result: ", data);
            }.bind(this),
            function (reason) {
              this.error("JSON error while saving to store ", reason);
            }.bind(this)
          );
        }.bind(this),
        function (reason) {
          this.error("Failed saving data", reason, key);
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
    console.log("Plain text editor created");
    this.update();
  },
  computed: {
    external_link() {
      if (typeof this.metadata.key == "string") {
        return this.url_store_data_prefix + this.metadata.key;
      } else {
        return this.url_query_prefix + this.metadata.query;
      }
    },
  },
};
</script>
<style lang="scss">
// required class
.highlighting-editor {
  background: #2d2d2d;
  color: #ccc;

  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  padding: 5px;
}

// optional
.prism-editor__textarea:focus {
  outline: none;
}
</style>
