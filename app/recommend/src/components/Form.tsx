import React, { useState } from 'react'
import IconButton from '@mui/material/IconButton';
import Paper from '@mui/material/Paper';
import Divider from '@mui/material/Divider';
import SearchIcon from '@mui/icons-material/Search';
import InputBase from '@mui/material/InputBase';

type FormPropsType = {
    setWord: React.Dispatch<React.SetStateAction<string>>;
    Search: (e:any) => void;
}

const Form = (props:FormPropsType) => {
    return (
    <form action="/search"> 
        <Paper
      component="form"
      sx={{ p: '2px 4px', display: 'flex', alignItems:'center', width: 400 }}
    >
        <InputBase
        sx={{ ml: 1, flex: 1 }}
        placeholder="例：飲み会　友達"
        onChange={e => props.setWord(e.target.value)}
      />
       <Divider sx={{ height: 28, m: 0.5 }} orientation="vertical" />
            <IconButton color="primary" aria-label="Search" component="label" onClick={props.Search} sx={{ p: '10px' }}>
                <SearchIcon/>
            </IconButton>
    </Paper>
    </form>
    );
};

export default Form;