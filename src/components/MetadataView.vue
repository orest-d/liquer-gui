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
        <v-expansion-panel-header>Info</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-simple-table>
            <tbody>
              <tr><td>Query</td><td>{{query}}</td></tr>
              <tr><td>Key</td><td>{{key}}</td></tr>
              <tr><td>Parent query</td><td>{{metadata.parent_query}}</td></tr>
              <tr><td>Type identifier</td><td>{{metadata.type_identifier}}</td></tr>
              <tr><td>Started</td><td>{{metadata.started}}</td></tr>
              <tr><td>Updated</td><td>{{metadata.updated}}</td></tr>
              <tr><td>Created</td><td>{{metadata.created}}</td></tr>
            </tbody>
          </v-simple-table>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-card>
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
    metadata: {
      default: null,
    },
  },
  data: () => ({
    panel: [0],
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