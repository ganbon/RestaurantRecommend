import Header from "./Header"
import SubTitle from "./SubTitle"
import Axios from 'axios'
import React, { useState } from 'react'
import Grid from '@mui/material/Unstable_Grid2';
import Shopdisplay from "./Shopdisplay"
import useLocationChange from "./LocationChange";

type ResultsPropsType = {
  url: "";
  name: "";
  genre: "";
  review: 0;
  place: "";
}
const Recommend = () => {
  const [lunch, setLunchResults] = useState<Array<ResultsPropsType>>([
  ]);
  const [dinner, setDinnerResults] = useState<Array<ResultsPropsType>>([
  ]);
  const GNNResult = () =>{
    Axios.post("http://127.0.0.1:5000/recommend")
    .then(res => {
        setLunchResults(res.data.lunch);
        setDinnerResults(res.data.dinner);
    })
  }
  useLocationChange(() => {
    GNNResult();
  })
    return(
      <>
        <Header title="あなたへのおすすめ"/>
        <SubTitle title="ランチ"/>
        <Grid container spacing={{ xs: 1, md: 2 }} columns={{ xs: 2, sm: 6, md: 12 }}>
        <Shopdisplay shoplist={lunch}/>
        </Grid>
        <SubTitle title="ディナー"/>
        <Grid container spacing={{ xs: 1, md: 2 }} columns={{ xs: 2, sm: 6, md: 12 }}>
        <Shopdisplay shoplist={dinner}/>
        </Grid>
      </>
    )
}

export default Recommend