import React from 'react';
import { List, Datagrid, DateField, TextField, ReferenceField, Edit, SimpleForm, ReferenceInput, TextInput, SelectInput } from 'react-admin';

export const TaskList = props => (
    <List {...props}>
        <Datagrid rowClick="edit">
            <TextField source="id" />
            <TextField source="url" />
            <ReferenceField source="user_id" reference="user">
                <TextField source="id" />
            </ReferenceField>
            <DateField source="added_time" />
            <DateField source="modify_time" />
            <TextField source="priority" />
            <TextField source="description" />
            <DateField source="schedule_time" />
            <DateField source="interval" />
        </Datagrid>
    </List>
);

export const TaskEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <ReferenceInput source="user_id" reference="user"><SelectInput optionText="id" /></ReferenceInput>
            <TextInput source="url" />
            <TextInput source="description" />
            <TextInput source="priority" />
        </SimpleForm>
    </Edit>
);