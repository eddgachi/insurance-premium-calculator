<!-- DashboardView.vue -->

<template>
  <div>
    <PremiumCalculator />
  </div>
</template>

<script>
import PremiumCalculator from '@/components/PremiumCalculator.vue'

export default {
  name: 'DashboardView',
  components: { PremiumCalculator },
}
</script>
