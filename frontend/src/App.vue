<!-- App.vue -->

<template>
  <div :class="['app-wrapper', { 'sidebar-open': isSidebarOpen }, themeClass]">
    <aside :class="['sidebar', theme === 'dark' ? 'bg-black' : 'bg-white', 'shadow-lg border-end']">
      <div class="p-3 d-flex justify-content-between align-items-center border-bottom">
        <h2 class="h6 mb-0 fw-semibold">Navigation</h2>
        <button
          class="btn btn-sm btn-close d-lg-none"
          @click="isSidebarOpen = false"
          aria-label="Close sidebar"
        ></button>
      </div>
      <div class="p-3 sidebar-nav">
        <ul class="list-unstyled">
          <li><router-link to="/" class="nav-link" :class="linkClass">Home</router-link></li>
          <li><router-link to="/requests" class="nav-link" :class="linkClass">Quote Requests</router-link></li>
          <li><router-link to="/results" class="nav-link" :class="linkClass">Quote Results</router-link></li>
        </ul>
      </div>
    </aside>
    <div v-if="isSidebarOpen" class="sidebar-backdrop d-lg-none" @click="isSidebarOpen = false"></div>

    <div class="main-content">
      <header :class="['shadow-sm sticky-top z-index-sticky', theme === 'dark' ? 'bg-black' : 'bg-white']">
        <div class="container-fluid px-4 py-2 d-flex justify-content-between align-items-center">
          <button class="btn btn-sm d-lg-none" @click="isSidebarOpen = !isSidebarOpen" aria-label="Toggle sidebar">
            <i :class="['fas fa-bars', theme === 'dark' ? 'text-light' : 'text-dark']"></i>
          </button>
          <h1 class="h6 mb-0 fw-semibold" :class="titleClass">Insurance Premium Calculator</h1>
          <button class="btn btn-sm" @click="toggleTheme" :class="theme === 'dark' ? 'text-warning' : 'text-dark'">
            <i :class="['fas', theme === 'dark' ? 'fa-sun' : 'fa-moon']"></i>
          </button>
        </div>
      </header>

      <main class="container-fluid p-4">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>

      <footer
        :class="[
          'mt-auto py-3 text-center small text-muted border-top',
          theme === 'dark' ? 'bg-black border-secondary' : 'bg-light border-light-subtle',
        ]"
      >
        © {{ new Date().getFullYear() }} Insurance Premium Calculator <br />
        made with ❤️
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      theme: 'light',
      isSidebarOpen: false,
    }
  },
  computed: {
    themeClass() {
      return this.theme === 'dark' ? 'bg-dark text-light' : 'bg-light'
    },
    linkClass() {
      return this.theme === 'dark' ? 'text-light' : 'text-dark'
    },
    titleClass() {
      return this.theme === 'dark' ? 'text-light' : 'text-dark'
    },
  },
  methods: {
    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light'
      document.body.setAttribute('data-bs-theme', this.theme)
      localStorage.setItem('dashboardTheme', this.theme)
    },
  },
  watch: {
    $route() {
      this.isSidebarOpen = false
    },
  },
  mounted() {
    const savedTheme = localStorage.getItem('dashboardTheme')
    if (savedTheme) this.theme = savedTheme
    document.body.setAttribute('data-bs-theme', this.theme)
  },
}
</script>

<style>
/* --- Global App Styles --- */
html,
body {
  height: 100%;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-wrapper {
  display: flex;
  min-height: 100vh;
}

/* --- Sidebar Styles --- */
.sidebar {
  width: 260px; /* Slightly wider */
  position: fixed;
  top: 0;
  left: -260px; /* Hidden by default on mobile */
  height: 100vh;
  transition: left 0.3s ease-in-out;
  z-index: 1050;
  overflow-y: auto;
}

.sidebar.open {
  /* Mobile open state */
  left: 0;
}

.sidebar-backdrop {
  /* Mobile backdrop */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1040;
}

.sidebar-nav .nav-link {
  padding: 0.5rem 0.8rem;
  margin-bottom: 0.1rem;
  border-radius: 0.375rem;
  font-size: 0.9rem;
  transition: background-color 0.2s ease, color 0.2s ease;
  display: flex;
  align-items: center;
}

/* Active link styling */
.sidebar-nav .nav-link.router-link-exact-active {
  background-color: var(--bs-primary-bg-subtle);
  color: var(--bs-primary-text-emphasis) !important; /* Ensure text color overrides */
  font-weight: 500;
}
[data-bs-theme='dark'] .sidebar-nav .nav-link.router-link-exact-active {
  background-color: var(--bs-primary);
  color: var(--bs-light) !important;
}

.sidebar-nav .nav-link:hover {
  background-color: var(--bs-secondary-bg);
}
[data-bs-theme='dark'] .sidebar-nav .nav-link:hover {
  background-color: var(--bs-dark-bg-subtle);
}

/* --- Main Content Area --- */
.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  min-width: 0; /* Important for flex item wrapping */
  transition: margin-left 0.3s ease-in-out;
}

@media (min-width: 992px) {
  /* lg breakpoint */
  .sidebar {
    left: 0; /* Always open on large screens */
    z-index: 1000; /* Below sticky header */
  }
  .main-content {
    margin-left: 260px; /* Push content over */
  }
  .app-wrapper.sidebar-collapsed .sidebar {
    left: -260px; /* Example for collapsing */
  }
  .app-wrapper.sidebar-collapsed .main-content {
    margin-left: 0;
  }
}

/* --- Router Transition --- */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* --- Helper Styles --- */
.z-index-sticky {
  z-index: 1020;
}

/* Minor adjustments if needed */
body {
  overflow-x: hidden; /* Prevent horizontal scrollbars caused by transitions */
}
</style>
