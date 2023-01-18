<template>
  <v-container>
    <v-card>
      <v-card-title
        >Upload File: &nbsp;&nbsp;&nbsp;<em>{{ new_key }}</em></v-card-title
      >
      <v-card-content>
        <v-form>
          <v-file-input
            show-size
            label="File input"
            @change="select_file"
            v-model="content"
          ></v-file-input>
          <v-text-field label="File name" v-model="file_name"></v-text-field>
          <v-text-field label="Title" v-model="title"></v-text-field>
          <v-textarea
            solo
            label="Description"
            rows="3"
            v-model="description"
          ></v-textarea>
        </v-form>
      </v-card-content>
      <v-card-actions>
        <v-btn @click="create()">Create</v-btn>
        <v-btn href="#-i-mode/store">Cancel</v-btn>
        <v-checkbox
          v-model="allow_overwrite"
          label="Allow overwrite"
        ></v-checkbox>
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
    file_name: "",
    title: "",
    description: "",
    content: "",
    current_file: null,
    result_metadata: { status: "", message: "" },
    result_data: { status: "", message: "" },
    allow_overwrite:false,
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
    select_file(file){
        console.log("select file", file);
        this.file_name=file.name;
        this.current_file=file;
    },
    create(){
        console.log("Create", this.file_name);
        if (this.allow_overwrite) {
            console.log("Allow overwrite", this.file_name);
            this.do_create();
        }
        else{
            this.$http.get(this.contains_url).then(
                function (response) {
                    response.json().then(
                        function (data) {
                            console.log("Contains result: ", data);
                            var contains = data.contains;
                            if (contains){
                                this.error("Key "+this.new_key+" exists. Allow overwrite to proceed.")
                            }
                            else{
                                this.do_create();
                            }
                        }.bind(this),
                        function (reason) {
                            this.error("JSON error while 'contains'", reason);
                        }.bind(this)
                    );
                }.bind(this),
                function (reason) {
                    this.error("Failed calling 'contains'", reason);
                }.bind(this)
            );
        }
    },
    do_create() {
      console.log("Do create", this.file_name);
      this.$http.post(this.create_metadata_url, this.metadata).then(
        function (response) {
          response.json().then(
            function (data) {
              this.result_metadata = data;
              this.info(data.message);
              console.log("Create metadata result: ", this.result);
              this.info("Uploading "+this.current_file);
              const form_data = new FormData();
              form_data.append('file', this.current_file);
              this.$http.post(this.upload_data_url, form_data).then(
                function (response) {
                  response.json().then(
                    function (data) {
                      this.result_metadata = data;
                      this.info(data.message);
                      console.log("Create data result: ", this.result);
                      window.location.href = "#-i-mode/store";
                    }.bind(this),
                    function (reason) {
                      this.error("JSON error while creating data", reason);
                    }.bind(this)
                  );
                }.bind(this),
                function (reason) {
                  this.error("Failed creating data", reason);
                }.bind(this)
              );
            }.bind(this),
            function (reason) {
              this.error("JSON error while creating metadata", reason);
            }.bind(this)
          );
        }.bind(this),
        function (reason) {
          this.error("Failed creating metadata", reason);
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
      key = key + this.file_name;
      return key;
    },
    create_metadata_url() {
      return this.liquer_url + "/api/store/metadata/" + this.new_key;
    },
    upload_data_url() {
      return this.liquer_url + "/api/store/upload/" + this.new_key;
    },
    contains_url() {
      return this.liquer_url + "/api/store/contains/" + this.new_key;
    },
    metadata() {
      return {
        query: "-R/" + this.new_key,
        key: this.new_key,
        status: "external",
        type_identifier: "text",
        message: "Created by user",
        is_error: false,
        log: [],
        child_log: [],
        title: this.title,
        description: this.description,
      };
    },
  },
};
</script>