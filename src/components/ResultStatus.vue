<template>
  <v-chip :color="color" dark class="ma-2"
      small outlined>
    <v-icon>{{icon}}</v-icon>{{status}}
  </v-chip>
</template>

<script>
export default {
  props: ["status"],
  data: () => ({
    table: {
      none: {color: 'gray', icon:'mdi-help-circle'},
      null: {color: 'gray', icon:'mdi-help-circle'},
      submitted: {color: 'blue', icon:'mdi-clock-outline'},
      parent: {color: 'yellow', icon:'mdi-pinwheel-outline'},
      evaluation: {color: 'yellow', icon:'mdi-pinwheel'},
      dependencies: {color: 'yellow', icon:'mdi-pinwheel-outline'},
      ready: {color: 'green',icon:'mdi-check-circle'},
      error: {color: 'red', icon:'mdi-alert-circle'},
      obsolete: {color: 'gray',icon:'mdi-check'},
      recipe: {color: 'blue', icon:'mdi-link'},
      "side-effect": {color: 'green', icon:'mdi-check-circle'},
    },
  }),
  computed: {
    color() {
        try{
            return this.table[this.status].color;
        }
        catch(e) {
            return this.table["none"].color;
        }
    },
    icon() {
        try{
            return this.table[this.status].icon;
        }
        catch(e) {
            return this.table["none"].icon;
        }
    },
  },
};
</script>