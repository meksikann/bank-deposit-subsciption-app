import React from 'react';
import axios from 'axios';
import Home from './Home';

const getEmojiVal = (num) => {
  if(num > 0.4) {
    return 1
  }

  if(num < -0.3) {
    return -1
  }

  return 0
};

export default class AppWrapper extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      text:'',
      rows:[],
      disable: false
    };

    this.handleTExtChange = this.handleTExtChange.bind(this);
    this.sendFeedback = this.sendFeedback.bind(this);
  }


  async sendFeedback() {
    this.setState({
      disable: true
    });
    const {text, rows} = this.state;
    // const backendUrl = 'http://c9d25618.ngrok.io/sentiment';
    const backendUrl = 'http://localhost:8282/sentiment';

    const response = await axios.get(backendUrl, {params: {text}});
    console.log('Result:', response);
    let emoji = getEmojiVal(response.data.score);

    const score = `% ${Math.abs(response.data.score.toFixed(2) * 100)}`;
    const magn = `% ${Math.abs(response.data.magn.toFixed(2) * 100)}`;
    rows.push(this.createData(response.data.text, emoji, score, magn));
    this.setState({
      rows,
      text:'',
      disable: false
    })
  }

  handleTExtChange(event) {
    this.setState({
      text: event.target.value
    })
  }

  createData(text, emoji, score, magn) {
    return { text, emoji, score, magn };
  }

  render() {
    const {rows, text, disable} = this.state;

    return (
      <div className='app-container'>
        {/*<Link to={'/'}>Home</Link>*/}
        {/*<Link to={'/about'}>About</Link>*/}
        {/*<Link to={'/about/subroute'}>Subcomponent</Link>*/}
        {/*{this.props.children}*/}
        <Home
            handleClick={this.sendFeedback}
            handleTExtChange={this.handleTExtChange}
            data={rows}
            textValue={text}
            disable={disable}
        />
      </div>
    )
  }
}
