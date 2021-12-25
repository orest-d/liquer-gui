<template>
  <v-row>
      <v-col cols="1">
        <v-chip :color="color" dark class="ma-2" label
            outlined>
            <v-icon left>{{icon}}</v-icon>{{item.kind}}
        </v-chip>
      </v-col>
      <v-col cols="3"><span class="text-caption">{{item.timestamp}}</span>
          <p v-if="has_origin">
              <a class="text-caption" :href="origin_href">{{item.origin}}</a>
          </p>
      </v-col>
      <v-col cols="8">
          {{item.message}}
          <p v-if="has_traceback"><pre>{{item.traceback}}</pre></p>
      </v-col>
  </v-row>
</template>

<script>
export default {
  props: ["item"],
  data: () => ({
    table: {
      none: { color: "gray", icon: "mdi-help-circle" },
      error: { color: "red", icon: "mdi-alert-circle" },
      warning: { color: "orange", icon: "mdi-alert" },
      info: { color: "green", icon: "mdi-information" },
      debug: { color: "blue", icon: "mdi-bug" },
    },
  }),
  computed: {
    color() {
      try {
        return this.table[this.item.kind].color;
      } catch (e) {
        return this.table["none"].color;
      }
    },
    icon() {
      try {
        return this.table[this.item.kind].icon;
      } catch (e) {
        return this.table["none"].icon;
      }
    },
    origin_href() {
      try {
        if (
          this.item.origin != undefined &&
          this.item.origin != null &&
          this.item.origin != ""
        ) {
          return "#-i-m/" + this.item.origin;
        } else {
          return "#-i-mode/metadata";
        }
      } catch (e) {
        return "#-i-mode/metadata";
      }
    },
    has_origin() {
      try {
        return (
          this.item.origin != undefined &&
          this.item.origin != null &&
          this.item.origin != ""
        );
      } catch (e) {
        return false;
      }
    },
    has_traceback() {
      try {
        return (
          this.item.traceback != undefined &&
          this.item.traceback != null &&
          this.item.traceback != ""
        );
      } catch (e) {
        return false;
      }
    },
  },
};
</script>