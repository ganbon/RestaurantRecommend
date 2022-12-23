import Title from "./Title"
import Form from "./Form"
import Result from "./Result"
// import './App.css';
import React, { useState } from 'react'
import Axios from 'axios'

type ResultsStateType = {
    url: any;
    name: any;
    genre: any;
    review: any;
    place: any;
}

const SearchPage = () => {
  // 入力用の変数の定義
  const [keyword,setWord] = useState<string>("");
  const [result, setResults] = useState<ResultsStateType>({
    url: "",
    name: "",
    genre: "",
    review: 0,
    place: "",
  })
  const Search = (e:any) => {
      e.preventDefault();
      Axios.post("http://127.0.0.1:5000/search", {sentence:keyword})
      .then(res => {
          setResults({url:res.data.url,name:res.data.name,genre:res.data.genre,review:res.data.review,place:res.data.place});
      })
  } 
  if(result.url===""){  
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
        <Result url={result.url} name={result.name} genre={result.genre} review={result.review} place={result.place}/>
    </div>
  );
}

export default SearchPage;
