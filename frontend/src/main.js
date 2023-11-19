import { createApp } from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import store from './store'

import 'vuetify/styles'

import router from './router'
import { Axios } from 'axios'

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}


axios.defaults.baseURL = 'http://120.46.80.149'

import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
})

axios.defaults.baseURL = 'http://120.46.80.149'

app.use(vuetify)
app.use(ElementPlus)
app.use(router)
app.use(VueAxios, axios)
app.use(store)
app.mount('#app')