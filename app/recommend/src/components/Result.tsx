import Popup from "./PopUp"
import React from 'react'
import { LinkPreview } from '@dhaiwat10/react-link-preview';
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
        <p>{props.genre}</p>
        <p>{props.review}</p>
        <p>{props.place}</p>
        {/* <LinkPreview url={props.url} width='400px' /> */}
        <Popup></Popup>
        </div>
    );
};

export default Result;