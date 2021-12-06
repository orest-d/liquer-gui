<template>
  <v-card>
    <v-card-title>
      Metadata {{metadata.query}}
      <v-spacer></v-spacer>
      <v-container>
          <v-row><v-col>Status</v-col><v-col><ResultStatus :status="metadata.parent_query"></ResultStatus></v-col></v-row>
          <v-row><v-col>Parent</v-col><v-col>{{metadata.parent_query}}</v-col></v-row>
      </v-container>
    </v-card-title>

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
    update(){

    }
  },
  computed: {
  },
  watch: {
    metadata() {
      this.update();
    },
  },
  created: function () {
  },
};
</script>