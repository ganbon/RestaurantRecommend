import Title from "./Title"
import Form from "./Form"
import Result from "./Result"
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
  const [results, setResults] = useState<Array<ResultsPropsType>>([
  ]);
  const Search = (e:any) => {
      e.preventDefault();
      Axios.post("http://127.0.0.1:5000/search", {sentence:keyword})
      .then(res => {
          setResults(res.data);
      })
  } 
  if(results.length===0){  
    return (
      <div className="search">
        <Title title="検索"/>
        <Form setWord={setWord} Search={Search}/>
    </div>
    );
  }
  return (
    <div className="search">
        <Title title={keyword+"の検索結果"} />
        <Form setWord={setWord} Search={Search}/>
        {results.map((result) => {
          return(
        <Result url={result.url} name={result.name} genre={result.genre} review={result.review} place={result.place}/>
          );
        })}
    </div>
  );
}

export default SearchPage;
