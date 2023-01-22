import React, { useState } from 'react'
import {Button}  from '@mui/material';
import Axios from 'axios'


const DelateButton = (props:any) => {
  const Delate = (e:any) => {
    e.preventDefault();
    Axios.post("http://127.0.0.1:5000/visited", {name:props.name})
  }
  return (
    <div>
    <Button variant="outlined" onClick={Delate}>
          削除
    </Button>
    </div>
  );
}


export default DelateButton;