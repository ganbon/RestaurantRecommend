import Result from "./Result"
import Grid from '@mui/material/Unstable_Grid2';
import React, { useState } from 'react'


type ShopdataType = {
  url: "";
  name: "";
  genre: "";
  review: 0;
  place: "";
}

type ResultPropsType = {
  shoplist:ShopdataType[];
}
const BookList :React.FC<ResultPropsType> = React.memo(({shoplist}) => {
  return(
    <>
    {shoplist.map((result) => { 
      return(
    <Grid xs={2} sm={4} md={3}>
    <Result url={result.url} name={result.name} genre={result.genre} review={result.review} place={result.place}/>
    </Grid>
      );
  })}
  </>
  )
})
export default BookList