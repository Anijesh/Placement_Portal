import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
    path: '/',
    name: 'login',
    component: LoginView
  },

  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/student',
    name: 'studentDashboard',
    component: () => import('../views/StudentDashboardView.vue')
  },
  {
    path: '/company',
    name: 'companyDashboard',
    component: () => import('../views/CompanyDashboardView.vue')
  },
  {
    path: '/admin',
    name: 'adminDashboard',
    component: () => import('../views/AdminDashboardView.vue')
  },
  ],
})

router.beforeEach((to, from, next) => {

  const token = localStorage.getItem("token")
  const role = localStorage.getItem("role")

  if (!token && to.path !== "/" && to.path !== "/register") {
    return next("/")
  }

  if (to.path === "/admin" && role !== "admin") {
    return next("/")
  }

  if (to.path === "/company" && role !== "company") {
    return next("/")
  }

  if (to.path === "/student" && role !== "student") {
    return next("/")
  }

  next()

})

export default router
