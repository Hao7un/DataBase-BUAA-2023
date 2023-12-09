
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
                    path: '/project/all',
                    name: 'allProject',
                    component: () => import('../views/project/AllProjectPage.vue')
                },
                {
                    path: '/project/my',
                    name: 'myProject',
                    component: () => import('../views/project/MyProjectPage.vue')
                },
                {
                    path: '/project/info/:projectId',
                    name: 'projectInfo',
                    component: () => import('../views/project/ProjectInfoPage.vue')
                },
                {
                    path: '/team/join',
                    name: 'joinTeam',
                    component: () => import('../views/team/JoinTeamPage.vue')
                },
                {
                    path: '/team/my',
                    name: 'myTeam',
                    component: () => import('../views/team/MyTeamPage.vue')
                },
                {
                    path: '/team/info/:teamId',
                    name: 'teamInfo',
                    component: () => import('../views/team/TeamInfoPage.vue')
                },
                {
                    path: '/recruitment/join',
                    name: 'joinRecruitment',
                    component: () => import('../views/recruitment/JoinRecruitmentPage.vue')
                },
                {
                    path: '/recruitment/my',
                    name: 'myRecruitment',
                    component: () => import('../views/recruitment/MyRecruitmentPage.vue')
                },
                {
                    path: '/user/info',
                    name: 'userInfo',
                    component: () => import('../views/user/UserInfoPage.vue')
                },
                {
                    path: '/user/volunteer-time',
                    name: 'volunteerTime',
                    component: () => import('../views/user/VolunteerTimePage.vue')
                },
                {
                    path: '/admin/manage',
                    name: 'admin',
                    component: () => import('../views/admin/AdminPage.vue'),
                },
                {
                    path: '/admin/teaminfo',
                    name: 'teamDetail',
                    component: () => import('../views/admin/TeamManagePage.vue')
                },
                {
                    path: '/admin/projectinfo',
                    name: 'projectAdmin',
                    component: () => import('../views/admin/ProjectManagePage.vue')
                },
                {
                    path: '/admin/projectlist',
                    name: 'projectlist',
                    component: () => import('../views/admin/ProjectListPage.vue')
                },
                {
                    path: '/admin/recruitment',
                    name: 'recruitment',
                    component: () => import('../views/admin/RecruitmentManagePage.vue')
                }
                
            ]
        },
    ]
})

import store from '../store'
router.beforeEach((to, from, next) => {
    const isLoggedIn = store.state.userId !== null;
    if (!isLoggedIn && to.path !== '/welcome') {
        next({path: "/welcome"})
    }
    else {
        next();
    }
})

export default router