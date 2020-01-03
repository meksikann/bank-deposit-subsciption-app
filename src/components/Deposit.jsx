import React from 'react';
import axios from 'axios';
import Button from '@material-ui/core/Button';
import config from '../config/client';

import UserForm from "./UserForm";
import Users from "./Users";

export default class Deposit extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            users: [],
            runningQuery: false
        };

        this.predict = this.predict.bind(this);
        this.addUser = this.addUser.bind(this);
    }

    async componentDidMount() {
        const res = await axios.get(`${config.endpoint}users`);
        this.setState({
            users: res.data
        })
    }

    async predict() {
        const {users} = this.state;

        this.setState({
            runningQuery: true
        });
        const res = await axios.post(`${config.endpoint}predict`, {users});

        this.setState({
            users: res.data,
            runningQuery: false
        })
    }

    addUser(event) {
        event.preventDefault();
        const data = new FormData(event.target);

        console.log(data.get('age'));
    //    TODO: add user to 'users' table
    }

    render() {
        const {users, runningQuery} = this.state;
        return (
            <div className='app-container'>
                <UserForm handleSubmit={this.addUser}/>
                <div style={{margin: '20px'}}>
                    <Users users={users}/>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={this.predict}
                        style={{marginTop: '20px'}}
                        disabled={runningQuery}
                    >
                        Predict deposit subscription
                    </Button>
                </div>
            </div>
        )
    }
}
