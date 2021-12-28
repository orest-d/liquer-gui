<template>
  <v-container>
    <v-card>
      <v-card-title>Clean</v-card-title>
      <v-card-content>
        <v-form>
          <v-checkbox v-model="errors" label="Errors"></v-checkbox>
          <v-checkbox
            v-model="expired"
            label="Expired store items"
          ></v-checkbox>
          <v-checkbox
            v-model="evaluation"
            label="Evaluated/unfinished items"
          ></v-checkbox>
          <v-checkbox
            v-model="recipes"
            label="Finished items with recipes"
          ></v-checkbox>
          <v-checkbox v-model="cache" label="Cache"></v-checkbox>
        </v-form>
        <v-sheet elevation="3" rounded class="ma-4">
          <p>
            <b>{{ result.status }}</b
            >&nbsp; {{ result.message }}
          </p>
          <p>
            <b>{{ cache_clean_result.status }}</b
            >&nbsp; {{ cache_clean_result.message }}
          </p>
        </v-sheet>
      </v-card-content>
      <v-card-actions>
        <v-btn color="error" @click="clean()">Clean</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
export default {
  props: [],
  data: () => ({
    errors: true,
    expired: false,
    evaluation: true,
    recipes: false,
    cache: false,
    result: { status: "", message: "" },
    cache_clean_result: { status: "", message: "" },
    url_query_prefix: "/liquer/q/",
    url_clean_cache: "/liquer/api/cache/clean",
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
    clean() {
      console.log("Clean");
      if (this.errors || this.expired || this.evaluation || this.recipes) {
        console.log("Run clean " + this.clean_url);
        this.$http.get(this.clean_url).then(
          function (response) {
            response.json().then(
              function (data) {
                this.result = data;
                console.log("clean result: ", this.result);
              }.bind(this),
              function (reason) {
                this.error("JSON error while cleaning", reason);
              }.bind(this)
            );
          }.bind(this),
          function (reason) {
            this.error("Failed calling clean", reason);
          }.bind(this)
        );
      }
      if (this.cache) {
        console.log("Run clean cache:" + this.url_clean_cache);
        this.$http.get(this.url_clean_cache).then(
          function (response) {
            response.json().then(
              function (data) {
                this.cache_clean_result = data;
                console.log("cache clean result: ", this.cache_clean_result);
              }.bind(this),
              function (reason) {
                this.error("JSON error while cleaning cache", reason);
              }.bind(this)
            );
          }.bind(this),
          function (reason) {
            this.error("Failed calling clean", reason);
          }.bind(this)
        );
      }
    },
  },
  computed: {
    clean_url() {
      var url = this.url_query_prefix + "ns-meta/root_key/clean";
      url = url + (this.errors ? "-t" : "-f");
      url = url + (this.expired ? "-t" : "-f");
      url = url + (this.evaluation ? "-t" : "-f");
      url = url + (this.recipes ? "-t" : "-f");
      url = url + "-t/result.json";
      return url;
    },
  },
};
</script>