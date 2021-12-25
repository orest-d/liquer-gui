<template>
  <v-card>
    <v-card-title v-if="!has_metadata">
      No Metadata {{ query }}
      <v-spacer></v-spacer>
    </v-card-title>
    <v-card-title v-if="has_metadata">
      <ResultStatus :status="metadata.status"></ResultStatus> {{ query }}
    </v-card-title>
    <v-expansion-panels v-if="has_metadata" v-model="panel" multiple>
      <v-expansion-panel>
        <v-expansion-panel-header>Description</v-expansion-panel-header>
        <v-expansion-panel-content>
          <h3>{{ title }}</h3>
          <em>{{ data_description }}</em>
          <br />
          <pre>{{ description }}</pre>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header>Progress</v-expansion-panel-header>
        <v-expansion-panel-content>
          <div v-html="metadata.html_preview"></div>
          <div>{{ metadata.message }}</div>
          <ProgressIndicator
            v-for="(item, index) in metadata.progress_indicators"
            :item="item"
            :key="index"
            color="primary"
          />
          <ProgressIndicator
            v-for="(item, index) in metadata.child_progress_indicators"
            :item="item"
            :key="index"
            color="secondary"
          />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header>Logs</v-expansion-panel-header>
        <v-expansion-panel-content>
          <h3>Log</h3>
          <v-container fluid>
            <LogEntry
              v-for="(item, index) in metadata.log"
              :item="item"
              :key="index"
            />
          </v-container fluid>
          <h3>Child Log</h3>
          <v-container>
            <LogEntry
              v-for="(item, index) in metadata.child_log"
              :item="item"
              :key="index"
            />
          </v-container>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header>Info</v-expansion-panel-header>
        <v-expansion-panel-content>
          <h3>Basic data</h3>
          <v-simple-table>
            <tbody>
              <tr>
                <td>Query</td>
                <td>{{ query }}</td>
              </tr>
              <tr>
                <td>Key</td>
                <td>{{ key }}</td>
              </tr>
              <tr>
                <td>Parent query</td>
                <td>{{ metadata.parent_query }}</td>
              </tr>
              <tr>
                <td>Type identifier</td>
                <td>{{ metadata.type_identifier }}</td>
              </tr>
              <tr>
                <td>MIME type</td>
                <td>{{ metadata.mimetype }}</td>
              </tr>
              <tr>
                <td>Started</td>
                <td>{{ metadata.started }}</td>
              </tr>
              <tr>
                <td>Updated</td>
                <td>{{ metadata.updated }}</td>
              </tr>
              <tr>
                <td>Created</td>
                <td>{{ metadata.created }}</td>
              </tr>
            </tbody>
          </v-simple-table>
          <h3>File Info</h3>
          <v-simple-table>
            <tbody>
              <tr>
                <td>Name</td>
                <td>{{ fileinfo.name }}</td>
              </tr>
              <tr>
                <td>Extension</td>
                <td>{{ metadata.extension }}</td>
              </tr>
              <tr>
                <td>File-system path</td>
                <td>{{ fileinfo.filesystem_path }}</td>
              </tr>
              <tr>
                <td>MD5 checksum</td>
                <td>{{ fileinfo.md5 }}</td>
              </tr>
            </tbody>
          </v-simple-table>
          <h3>Recipe</h3>
          <v-simple-table>
            <tbody>
              <tr>
                <th colspan="2">Recipe</th>
              </tr>
              <tr>
                <td>Has recipe</td>
                <td>{{ metadata.has_recipe }}</td>
              </tr>
              <tr>
                <td>Recipes key</td>
                <td>{{ metadata.recipes_key }}</td>
              </tr>
              <tr>
                <td>Recipes directory</td>
                <td>{{ metadata.recipes_directory }}</td>
              </tr>
              <tr>
                <td>Is side-effect</td>
                <td>{{ metadata.side_effect }}</td>
              </tr>
            </tbody>
          </v-simple-table>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-card>
</template>

<script>
import ResultStatus from "./ResultStatus";
import ProgressIndicator from "./ProgressIndicator";
import LogEntry from "./LogEntry";

export default {
  components: {
    ResultStatus,
    ProgressIndicator,
    LogEntry,
  },
  props: {
    liquer_url: {
      type: String,
      default: "/liquer",
    },
    metadata: {
      default: null,
    },
  },
  data: () => ({
    panel: [0, 1],
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
    update() {},
  },
  computed: {
    has_metadata() {
      try {
        return "status" in this.metadata || "query" in this.metadata;
      } catch {
        return false;
      }
    },
    query() {
      try {
        return this.metadata.query;
      } catch {
        return "-na-";
      }
    },
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
    fileinfo() {
      console.log("Get fileinfo");
      try {
        var f = this.metadata.fileinfo;
        if (f == undefined || f == null) {
          console.log("fileinfo undefined");
          return {};
        } else {
          console.log("fileinfo OK");
          return f;
        }
      } catch {
        console.log("fileinfo error");
        return {};
      }
    },
    data_description() {
      try {
        return this.metadata.data_characteristics.description;
      } catch {
        return "";
      }
    },
  },
  watch: {
    metadata() {
      this.update();
    },
  },
  created: function () {},
};
</script>