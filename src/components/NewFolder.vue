<template>
  <v-container>
    <v-card>
      <v-card-title
        >New File: &nbsp;&nbsp;&nbsp;<em>{{ new_key }}</em></v-card-title
      >
      <v-card-content>
        <v-form>
          <v-text-field label="Folder name" v-model="folder_name"></v-text-field>
        </v-form>
      </v-card-content>
      <v-card-actions>
        <v-btn @click="create()">Create</v-btn>
        <v-btn href="#-i-mode/store">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
export default {
  props: {
    liquer_url: {
      type: String,
      default: "/liquer",
    },
    dirkey: {
      default: "",
    },
  },
  data: () => ({
    folder_name: "",
    result_data: { status: "", message: "" },
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
    create() {
        console.log("Create", this.folder_name);
        this.$http.get(this.create_url).then(
        function (response) {
            response.json().then(
            function (data) {
                this.result_metadata = data;
                this.info(data.message);
                console.log("Create folder result: ", this.result);
                window.location.href = "#-i-mode/store";
            }.bind(this),
            function (reason) {
                this.error("JSON error while creating folder "+this.new_key, reason);
            }.bind(this)
            );
        }.bind(this),
        function (reason) {
            this.error("Failed creating data", reason);
        }.bind(this)
        );
    },
  },
  computed: {
    new_key() {
      var key = "";
      if (this.dirkey.startsWith("/")) {
        key = key + this.dirkey.substring(1);
      } else {
        key = key + this.dirkey;
      }
      if (!key.endsWith("/")) {
        key = key + "/";
      }
      key = key + this.folder_name;
      return key;
    },
    create_url() {
      return this.liquer_url + "/api/store/makedir/" + this.new_key;
    },
  },
};
</script>