import Popup from "./PopUp"
import React from 'react'
import {Button,CardActionArea,CardActions} from '@mui/material';

type ResultsPropsType = {
    url: any;
    name: any;
    genre: any;
    review: any;
    place: any;
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