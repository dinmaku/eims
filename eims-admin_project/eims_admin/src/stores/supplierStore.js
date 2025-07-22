import { defineStore } from 'pinia';

export const useSupplierStore = defineStore('supplier', {
  state: () => ({
    totalSuppliers: 0
  }),
  actions: {
    setTotalSuppliers(count) {
      this.totalSuppliers = count;
    }
  }
});