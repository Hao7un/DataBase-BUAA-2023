
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
                    path: '/team/join',
                    name: 'joinTeam',
                    component: () => import('../views/joinTeamPage.vue')
                },
                {
                    path: '/recruitment/join',
                    name: 'joinRecruitment',
                    component: () => import('../views/JoinRecruitmentPage.vue')
                }
            ]
        },
    ]
})

export default router