
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
                    path: '/project/my',
                    name: 'myProject',
                    component: () => import('../views/MyProjectPage.vue')
                },
                {
                    path: '/project/info/:projectId',
                    name: 'projectInfo',
                    component: () => import('../views/ProjectInfoPage.vue')
                },
                {
                    path: '/team/join',
                    name: 'joinTeam',
                    component: () => import('../views/JoinTeamPage.vue')
                },
                {
                    path: '/team/my',
                    name: 'myTeam',
                    component: () => import('../views/MyTeamPage.vue')
                },
                {
                    path: '/team/info/:teamId',
                    name: 'teamInfo',
                    component: () => import('../views/TeamInfoPage.vue')
                },
                {
                    path: '/recruitment/join',
                    name: 'joinRecruitment',
                    component: () => import('../views/JoinRecruitmentPage.vue')
                },
                {
                    path: '/recruitment/my',
                    name: 'myRecruitment',
                    component: () => import('../views/MyRecruitmentPage.vue')
                },
                {
                    path: '/user/info',
                    name: 'userInfo',
                    component: () => import('../views/UserInfoPage.vue')
                },
                {
                    path: '/user/password',
                    name: 'password',
                    component: () => import('../views/PasswordPage.vue')
                },
                {
                    path: '/user/volunteer-hours',
                    name: 'volunteerHours',
                    component: () => import('../views/VolunteerHoursPage.vue')
                },
                {
                    path: '/admin/manage',
                    name: 'admin',
                    component: () => import('../views/AdminPage.vue'),
                },
                {
                    path: '/admin/teaminfo',
                    name: 'teamDetail',
                    component: () => import('../views/TeamManagePage.vue')
                },
                {
                    path: '/admin/projectinfo',
                    name: 'projectInfo',
                    component: () => import('../views/ProjectManagePage.vue')
                }
            ]
        },
    ]
})

export default router