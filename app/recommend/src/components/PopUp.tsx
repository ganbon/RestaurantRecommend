import React, { useState } from 'react'
import SubTitle from "./SubTitle"
import { Rating,Dialog,Button } from '@mui/material';
import DialogActions from '@mui/material/DialogActions';
import DialogTitle from '@mui/material/DialogTitle';
import Axios from 'axios'


const PopUp = (props:any) => {
  const [open, setOpen] = React.useState(false);
  const [lunchvalue, setLunchValue] = React.useState<number | null>(0);
  const [dinnervalue, setDinnerValue] = React.useState<number | null>(0);
  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };
  const Review = (e:any) => {
    e.preventDefault();
    Axios.post("http://127.0.0.1:5000/search", {name:props.name,lunch:lunchvalue,dinner:dinnervalue})
  }
  return (
    <div>
    <Button variant="outlined" onClick={handleClickOpen}>
          ブックマーク
    </Button>
    <Dialog onClose={handleClose} open={open}>
      <DialogTitle>レビュー</DialogTitle>
      <SubTitle title="ランチ"/>
      <Rating
          name="half-rating"
          defaultValue={0}
          precision={0.5}
          value={lunchvalue}
          onChange={(event, newlunchValue) => {
          setLunchValue(newlunchValue);
          }}
      />
      <SubTitle title="ディナー"/>
      <Rating
          name="half-rating"
          value={dinnervalue}
          defaultValue={0}
          precision={0.5}
          onChange={(event, newdinnerValue) => {
          setDinnerValue(newdinnerValue);
          }}
      />
      <DialogActions>
      <Button onClick={handleClose}>閉じる</Button>
      <Button onClick={() => {handleClose; Review;}}>決定</Button>
      </DialogActions>
    </Dialog>
    </div>
  );
}

export default PopUp;