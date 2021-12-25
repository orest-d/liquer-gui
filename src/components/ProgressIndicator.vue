<template>
  <p>
    <v-progress-linear
      v-if="item.total_steps != null"
      v-model="percentage"
      :color="color"
      height="25"
    >
      <span>{{ item.message }}</span>
    </v-progress-linear>
    <v-progress-circular
      v-if="item.total_steps == null"
      indeterminate
      :color="color"
    >
    </v-progress-circular>
    <span v-if="item.total_steps == null">{{ item.message }}</span>
  </p>
</template>

<script>
export default {
  props: ["item","color"],
  data: () => ({
  }),
  computed: {
      percentage(){
          return (this.item.step * 100) / this.item.total_steps;
      }
  },
};
</script>