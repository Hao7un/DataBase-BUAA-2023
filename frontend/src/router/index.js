
import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: '/welcome'
        },
        {
            path: '/welcome',
            name: 'welcome',
            component: () => import('../views/WelcomePage.vue')
        },
        {
            path: '/home',
            name: 'home',
            component: () => import('../views/HomePage.vue'),
            children: [
                {
                    path: '/project/join',
                    name: 'joinProject',
                    component: () => import('../views/JoinProjectPage.vue')
                },
                {
                    path: '/project/myproject',
                    name: 'myProject',
                    component: () => import('../views/MyProjectPage.vue')
                },
                {
                    path: '/team',
                    name: 'team',
                    component: () => import('../views/TeamPage.vue')
                }
            ]
        },
        
    ]
})

export default router