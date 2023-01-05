import Header from "./Header"
import Form from "./Form"
import Grid from '@mui/material/Unstable_Grid2';
import Shopdisplay from "./Shopdisplay"
import Container from '@mui/material/Container';
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
          setTitle(keyword);
      })
    } 
  if(keytitle===""){  
    return (
      <>
        <Header title="検索"/>
        <Container maxWidth="sm">
        <Form setWord={setWord} Search={Search}/>
        </Container>
    </>
    );
  }
  else{
  return (
    <>
        <Header title={keytitle+"の検索結果"} />
        <Container maxWidth="sm">
        <Form setWord={setWord} Search={Search}/>
        </Container>
        <Grid container spacing={{ xs: 1, md: 2 }} columns={{ xs: 2, sm: 6, md: 12 }}>
        <Shopdisplay shoplist={results}/>
      </Grid>
    </>
  );
  }
}
export default SearchPage;