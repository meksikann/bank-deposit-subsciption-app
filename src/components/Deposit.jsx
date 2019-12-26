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
    }

    async componentDidMount() {
        const res = await axios.get(`${config.endpoint}users`);
        this.setState({
            users: res.data
        })
    }

    predict() {
        const {users} = this.state;
        console.log(users);
        this.setState({
            runningQuery: true
        })
    }

    render() {
        const {users, runningQuery} = this.state;
        return (
            <div className='app-container'>
                <UserForm/>
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
