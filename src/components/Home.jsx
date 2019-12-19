import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import LinearProgress from '@material-ui/core/LinearProgress';
import SentimentVeryDissatisfiedIcon from '@material-ui/icons/SentimentVeryDissatisfied';
import SentimentVerySatisfiedIcon from '@material-ui/icons/SentimentVerySatisfied';
import SentimentSatisfiedIcon from '@material-ui/icons/SentimentSatisfied';


const StyledTableCell = withStyles(theme => ({
    head: {
        backgroundColor: theme.palette.common.black,
        color: theme.palette.common.white,
    },
    body: {
        fontSize: 14,
    },
}))(TableCell);

const StyledTableRow = withStyles(theme => ({
    root: {
        '&:nth-of-type(odd)': {
            backgroundColor: theme.palette.background.default,
        },
    },
}))(TableRow);



const Home = ({handleClick, handleTExtChange, data, textValue, disable}) => (
  <div className='home'>
      <div className='col'>
          <div><h3 style={{marginTop:'150px', marginLeft:'200px'}}>Feedback analyzer:</h3></div>
          <div>
              <TextField
                  id="outlined-multiline-static"
                  label="Please type feedback"
                  multiline
                  rows="4"
                  variant="outlined"
                  style={{margin: '20px', width:'600px'}}
                  onChange={handleTExtChange}
                  value={textValue}
              />
          </div>
          <Button
              variant="contained"
              color='primary'
              style={{margin:'20px', width:'100px'}}
              onClick={handleClick}
              disabled={disable}
          >
              Send
          </Button>
          {disable && <div>
              <LinearProgress variant="query" />
              <LinearProgress variant="query" color="secondary" />
          </div>}

          <div><h3 style={{marginLeft:'200px'}}>Sentiment analysis results:</h3></div>
          <div style={{margin: '20px'}}>
              <TableContainer component={Paper}>
                  <Table  aria-label="customized table">
                      <TableHead>
                          <TableRow>
                              <StyledTableCell align="left">Text</StyledTableCell>
                              <StyledTableCell align="right"> Emoji</StyledTableCell>
                              <StyledTableCell align="right">Score</StyledTableCell>
                              <StyledTableCell align="right">Magnitude</StyledTableCell>
                          </TableRow>
                      </TableHead>
                      <TableBody>
                          {data.map(row => (
                              <StyledTableRow key={row.text}>
                                  <StyledTableCell align="left">{row.text}</StyledTableCell>
                                  <StyledTableCell align="right">
                                      {row.emoji === 1 && <SentimentVerySatisfiedIcon color='primary'/>}
                                      {row.emoji === 0 && <SentimentSatisfiedIcon color='action'/>}
                                      {row.emoji === -1 && <SentimentVeryDissatisfiedIcon color='error'/>}
                                  </StyledTableCell>
                                  <StyledTableCell align="right">{row.score}</StyledTableCell>
                                  <StyledTableCell align="right">{row.magn}</StyledTableCell>
                              </StyledTableRow>
                          ))}
                      </TableBody>
                  </Table>
              </TableContainer>
          </div>
      </div>
  </div>
);

export default Home;
