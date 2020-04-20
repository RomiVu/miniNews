import decodeJwt from 'jwt-decode';

const authProvider = {
    login: ({ username, password }) =>  {
        const body = encodeURIComponent("username") + '=' + encodeURIComponent(username) + '&' +
                     encodeURIComponent("password") + '=' + encodeURIComponent(password);
        const request = new Request('http://localhost:8000/token', {
            method: 'POST',
            headers: new Headers({ 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' }),
            body,
        });
        return fetch(request)
            .then(response => {
                if (response.status < 200 || response.status >= 300) {
                    throw new Error(response.statusText);
                }
                return response.json();
            })
            .then(({ access_token }) => {
                const decodedToken = decodeJwt(access_token);
                localStorage.setItem('token', access_token);
                localStorage.setItem('role', decodedToken.role);
            });
    },
    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        return Promise.resolve();
    },
    checkError: (error) => {
        const status = error.status;
        if (status === 401 || status === 403) {
            localStorage.removeItem('token');
            localStorage.removeItem('role');
            return Promise.reject();
        }
        return Promise.resolve();
    },
    checkAuth: () => localStorage.getItem('token')
        ? Promise.resolve()
        : Promise.reject(),
    getPermissions: () => {
        const role = localStorage.getItem('role');
        return role === 'test_admin' ? Promise.resolve(role) : Promise.reject();
    },
};

export default authProvider;