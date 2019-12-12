import React from 'react';
import { Link } from 'react-router-dom';
import Deposit from "./Deposit";

export default class AppWrapper extends React.Component {
  render() {
    return (
      <div className='app-container'>
        <Deposit />
      </div>
    )
  }
}
