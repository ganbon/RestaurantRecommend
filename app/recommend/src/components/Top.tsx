import Title from "./Title"
import Search from "./Search"
import React, { useState } from 'react'
import Button from '@mui/material/Button';
import { NavLink } from "react-router-dom";


const Top = () =>{
    return (
      <div>
        <Title title={"グルメコンサルティング"}/>
        <Button href="/search">検索</Button>
        <Button href="/new">あなたへのおすすめ</Button>
        <Button href="/popular">人気のお店</Button>
      </div>
    );
}

export default Top