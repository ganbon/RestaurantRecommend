import Header from "./Header"
import SubTitle from "./SubTitle"
import Axios from 'axios'
import React, { useState } from 'react'
import Grid from '@mui/material/Unstable_Grid2';
import Shopdisplay from "./Shopdisplay"
import Container from '@mui/material/Container';
import useLocationChange from "./LocationChange";
import Loading from "./Laoding";


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
  const [ isLoading, setIsLoading ] = useState(false);
  const GNNResult = () =>{
    setIsLoading(true);
    Axios.post("http://127.0.0.1:5000/recommend")
    .then(res => {
        setLunchResults(res.data.lunch);
        setDinnerResults(res.data.dinner);
        setIsLoading(false);
    })
  }
  useLocationChange(() => {
    GNNResult();
  })
    return(
      <>
        <Header title="あなたへのおすすめ"/>
        <SubTitle title="ランチ"/>
        { isLoading ? <Container maxWidth="sm"><Loading /></Container>:
        <Grid container spacing={{ xs: 1, md: 2 }} columns={{ xs: 2, sm: 6, md: 12 }}>
        <Shopdisplay shoplist={lunch}/>
        </Grid>}
        <SubTitle title="ディナー"/>
        { isLoading ? <Container maxWidth="sm"><Loading /></Container>:
        <Grid container spacing={{ xs: 1, md: 2 }} columns={{ xs: 2, sm: 6, md: 12 }}>
        <Shopdisplay shoplist={dinner}/>
        </Grid>
        }
      </>
    )
}

export default Recommend