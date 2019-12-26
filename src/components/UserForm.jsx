import React from 'react';
import TextField from '@material-ui/core/TextField';

import Button from '@material-ui/core/Button';

const UserForm = (props) => (
  <div style={{margin: '20px'}}>
      <h5>New user:</h5>
      <form  onSubmit={props.handleSubmit} noValidate autoComplete="off">
          <div >
              <TextField
                  id="age"
                  label="age"
                  name="age"
                  variant="outlined"
                  type="number"

              />
              <TextField
                  id="job"
                  label="job"
                  name="job"
                  variant="outlined"
              />
              <TextField
                  id="marital"
                  label="marital"
                  name="marital"
                  variant="outlined"
              />
              <TextField
                  id="job"
                  label="job"
                  name="job"
                  variant="outlined"
              />
              <TextField
                  id="education"
                  label="education"
                  name="education"
                  variant="outlined"
              />
          </div>
          <Button type={'submit'}
              variant="contained"
              color="primary"

              style={{marginTop: '20px'}}
          >
              Add user
          </Button>
      </form>
  </div>
);

export default UserForm;
