import Title from "./Title"
import Axios from 'axios'
import Result from "./Result"
import React, { useState } from 'react'
type ResultsStateType = {
  url: any;
  name: any;
  genre: any;
  review: any;
  place: any;
}
const Recommend = () => {
  const [result, setResults] = useState<ResultsStateType>({
    url: "",
    name: "",
    genre: "",
    review: 0,
    place: "",
    })
const GNNResult = (e:any) =>{
    e.preventDefault();
      Axios.post("http://127.0.0.1:5000/gnn")
      .then(res => {
          setResults({url:res.data.url,name:res.data.name,genre:res.data.genre,review:res.data.review,place:res.data.place});
      })
}
    return(
      <div className="App">
        <Title title="あなたへのおすすめ"/>
        <Result url={result.url} name={result.name} genre={result.genre} review={result.review} place={result.place}/>
    </div>
    )
}

export default Recommend;