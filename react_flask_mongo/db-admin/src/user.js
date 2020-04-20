import React from 'react';
import { List, Datagrid, TextField, EmailField, DateField } from 'react-admin';


export const UserList = props => (
    <List {...props}>
        <Datagrid rowClick="edit">
            <TextField source="id" />
            <TextField source="username" />
            <EmailField source="email" />
            <TextField source="phone" />
            <DateField source="vaild_before" />
            <DateField source="last_seen" />
        </Datagrid>
    </List>
);