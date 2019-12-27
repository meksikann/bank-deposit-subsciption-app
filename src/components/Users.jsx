import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const columnNames = ["age", "job", "marital", "education", "default", "balance", "housing", "loan", "contact", "day",
        "month", "duration", "campaign", "pdays", "previous", "poutcome", "predicted", "actual_subscription"];

const renderItems = (items, names) => {
    return (
        <TableBody>
            {items.map((row, i) => (
                <TableRow key={i} hover>
                    <TableCell>{i}</TableCell>
                    {names.map(name => {
                        let styles = {};
                        if(name === 'subscription') {
                           styles.color = 'red'
                        }

                        return (
                        <TableCell key={name+i} align="left" style={styles}>
                            {row[name]}
                        </TableCell>
                    )})}
                </TableRow>
            ))}
        </TableBody>
    )
};

const renderHeader = (names) => {
    return names.map(name => (
        <TableCell key={name}><h4 style={{textTransform: 'capitalize'}}>{name}</h4></TableCell>
    ));
};

const Users = (props) => (
    <div className='about'>
        <h3 style={{textAlign:'center'}}>Bank Clients:</h3>
        <TableContainer component={Paper}>
            <Table aria-label="table">
                <TableHead>
                    <TableRow>
                        <TableCell key={'№'}><h4 style={{textTransform: 'capitalize'}}>№</h4></TableCell>
                        {renderHeader(columnNames)}
                    </TableRow>
                </TableHead>
                {renderItems(props.users, columnNames)}
            </Table>
        </TableContainer>
    </div>
);

export default Users;
