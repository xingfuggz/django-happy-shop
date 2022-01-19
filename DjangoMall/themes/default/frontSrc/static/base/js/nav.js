var nav = new Vue({
    el: "#nav",
    // 修改Vue变量的读取语法，避免与django冲突
    delimiters: ['[[', ']]'],
    data: {
        name: username,
        navigation: 'home',
        cartNum: cartNum
    },
    methods: {
        // 退出登录确认弹窗
        logout() {
            this.$buefy.dialog.confirm({
                message: '你确定要退出吗？',
                cancelText: '取消',
                confirmText: '确认',
                onConfirm: () => {
                    axios.get('/users/logout/').then(() => {
                        console.log('ceshi')
                        this.$buefy.toast.open('退出成功!')
                        setTimeout("window.location.reload()", 2000)
                        // window.location.href = '/users/login/';
                    })
                }
            })
        },
    },
})