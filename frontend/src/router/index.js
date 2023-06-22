import { createRouter, createWebHistory } from 'vue-router'
import LoginForm from '../components/Login.vue'
import CreateForm from '../components/signup.vue'
import NewsFeed from '../components/dashboard.vue'
import UserProfile from '../components/profile.vue'
import OtherProfile from '../components/other.vue'
const routes = [
  
  {
    path:'/',
    name:'login',
    component:LoginForm
  },
  {
    path:'/signup',
    name:'signup',
    component:CreateForm
  },
  {
    path:'/newsfeed',
    name:'newsfeed',
    component:NewsFeed
  },
  {
    path:'/profile',
    name:'profile',
    component:UserProfile
  },
  {
    path:'/other/:user_id',
    name:'other',
    component:OtherProfile
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
