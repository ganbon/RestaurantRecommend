import Title from "./Title"
import Form from "./Form"
import Result from "./Result"
import Grid from '@mui/material/Unstable_Grid2';
// import './App.css';
import React, { useState } from 'react'
import Axios from 'axios'

type ResultsPropsType = {
  url: "";
  name: "";
  genre: "";
  review: 0;
  place: "";
}


const SearchPage = () => {
  // 入力用の変数の定義
  const [keyword,setWord] = useState<string>("");
  const [keytitle,setTitle] = useState<string>("");
  const [results, setResults] = useState<Array<ResultsPropsType>>([
  ]);
  const Search = (e:any) => {
      e.preventDefault();
      Axios.post("http://127.0.0.1:5000/search", {sentence:keyword})
      .then(res => {
          setResults(res.data);
      })
      setTitle(keyword);
  } 
  if(keytitle===""){  
    return (
      <>
        <Title title="検索"/>
        <Form setWord={setWord} Search={Search}/>
    </>
    );
  }
  else{
  return (
    <>
        <Title title={keytitle+"の検索結果"} />
        <Form setWord={setWord} Search={Search}/>
        <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
        {results.map((result) => { 
          return(
        <Grid>
        <Result url={result.url} name={result.name} genre={result.genre} review={result.review} place={result.place}/>
        </Grid>
          );
      })}
      </Grid>
    </>
  );
  }
}
export default SearchPage;