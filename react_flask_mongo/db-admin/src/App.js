import React from 'react';
import { fetchUtils, Admin, Resource } from 'react-admin';
import simpleRestProvider from 'ra-data-json-server';
import { UserList } from './user';
import { TaskList } from './task';
import Dashboard from './Dashboard';
import authProvider from './authProvider';

const fetchJson = (url, options = {}) => {
    if (!options.headers) {
        options.headers = new Headers({ Accept: 'application/json' });
    }
    // add your own headers here
    let token = localStorage.getItem('token');
    options.headers.set('Authorization', 'Bearer ' + token);
    return fetchUtils.fetchJson(url, options);
}

const dataProvider = simpleRestProvider('http://127.0.0.1:8000', fetchJson);

const App = () => (
    <Admin dataProvider={ dataProvider } dashboard={Dashboard} authProvider={authProvider}>
        <Resource name="task" list={TaskList} />
        <Resource name="user" list={UserList} />
    </Admin>
);

export default App;