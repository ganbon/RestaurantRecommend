import Title from "./Title"
import SubTitle from "./SubTitle"
import Axios from 'axios'
import Result from "./Result"
import React, { useState } from 'react'

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
const GNNResult = (e:any) =>{
    e.preventDefault();
      Axios.post("http://127.0.0.1:5000/gnn")
      .then(res => {
          setLunchResults(res.data.lunch);
          setDinnerResults(res.data.dinner);
      })
}
    return(
      <div className="Recommend">
        <Title title="あなたへのおすすめ"/>
        <SubTitle title="ランチ"/>
        {lunch.map((result) => {
          return(
        <Result url={result.url} name={result.name} genre={result.genre} review={result.review} place={result.place}/>
          );
        })}
        <SubTitle title="ディナー"/>
        {dinner.map((result) => {
          return(
        <Result url={result.url} name={result.name} genre={result.genre} review={result.review} place={result.place}/>
          );
        })}
    </div>
    )
}

export default Recommend