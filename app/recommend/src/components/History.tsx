import BookList from "./BookList";
import Axios from 'axios'
import Header from "./Header";
import React, { useState } from 'react'
import useLocationChange from "./LocationChange";

type ResultsPropsType = {
    url: "";
    name: "";
    genre: "";
    review: 0;
    place: "";
  }
  const History = () => {
    const [book, Results] = useState<Array<ResultsPropsType>>([
    ]);
    const History = () =>{
      Axios.post("http://127.0.0.1:5000/history")
      .then(res => {
          Results(res.data);
      })
    }
    useLocationChange(() => {
      History();
    })
      return(
        <>
          <Header title="履歴"/>
          <BookList shoplist={book}/>
        </>
      )
  }
  
  export default History