<template>
  <v-card v-if="commands != null">
    <v-card-title>
      List of commands
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      >
      </v-text-field>
    </v-card-title>

    <v-data-table
      :headers="commands_headers"
      :items="commands_rows"
      :search="search"
      class="elevation-1"
    >
      <template v-slot:item.name="{ item }">
        <a :href="'#-i-q/ns-meta/help-' + item.name + '-' + item.ns">{{
          item.name
        }}</a>
      </template>
      <template v-slot:item.example_link="{ item }">
        <a v-if="item.example_link" :href="'#' + item.example_link">{{
          item.example_link
        }}</a>
      </template>
      <template v-slot:item.doc="{ item }">
        {{ item.doc.split("\n")[0] }}
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  props: {
    liquer_url: {
      type: String,
      default: "/liquer",
    },
  },
  data: () => ({
    commands: [],
    search: "",
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
  },
  computed: {
    commands_headers() {
      return [
        { text: "Namespace", value: "ns" },
        { text: "Command", value: "name" },
        { text: "Description", value: "doc" },
        { text: "Example", value: "example_link" },
      ];
    },
    commands_rows() {
      if (this.commands == null) {
        return [];
      } else {
        return this.commands;
      }
    },
  },

  created: function () {
    this.info("Hello from commands");

    this.$http
      .get(this.liquer_url + "/q/ns-meta/flat_commands/commands.json")
      .then(
        function (response) {
          response.json().then(
            function (data) {
              this.commands = data;
              this.info("Commands loaded.");
            }.bind(this),
            function (reason) {
              this.error("Json error (commands)", reason);
            }.bind(this)
          );
        }.bind(this),
        function (reason) {
          this.error("Data loading error", reason);
        }.bind(this)
      );
  },
};
</script>