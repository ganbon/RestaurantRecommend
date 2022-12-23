import Popup from "./PopUp"
import React from 'react'
import {Button,CardActionArea,CardActions} from '@mui/material';

type ResultsPropsType = {
    url: "";
    name: "";
    genre: "";
    review: 0;
    place: "";
  }

const Result = (props:ResultsPropsType) => {
    return (
        <div className="shop_data">
        <h2>{props.name}</h2>
        <a>{props.url}</a>
        <p>{props.genre}</p>
        <p>{props.review}</p>
        <p>{props.place}</p>
        <Popup></Popup>
        </div>
    );
};

export default Result;