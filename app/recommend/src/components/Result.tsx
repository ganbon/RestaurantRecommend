import * as React from 'react';
import Popup from "./PopUp"
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Rating from '@mui/material/Rating';
import { Button, CardActionArea, CardActions } from '@mui/material';

type ResultsPropsType = {
    url: "";
    name: "";
    genre: "";
    review: 0;
    place: "";
  }

const Result = (props:ResultsPropsType) => {
    return (
        <Card sx={{ maxWidth: 345 }}>
        <CardActionArea>
          <CardMedia
            component="img"
            height="140"
            image={`${process.env.PUBLIC_URL}/image/''.png`}
            alt="green iguana"
          />
          <CardContent>
            <Typography gutterBottom variant="h5" component="div">
              {props.name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              ジャンル：{props.genre}
              場所：{props.place}
              <Rating name="read-only" value={props.review} precision={0.25} readOnly />
            </Typography>
          </CardContent>
        </CardActionArea>
        <CardActions>
        <Popup name={props.name}/>
      </CardActions>
      </Card>
      );
}


export default Result;