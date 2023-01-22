import React, { useState } from 'react'
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
    Axios.post("http://127.0.0.1:5000/visited", {name:props.name,lunch:lunchvalue,dinner:dinnervalue})
  }
  return (
    <div>
    <Button variant="outlined" onClick={handleClickOpen}>
          ブックマーク
    </Button>
    <Dialog onClose={handleClose} open={open}>
      <DialogTitle sx={{ m: 0, p: 2 }}>レビュー</DialogTitle>
    <p>ランチ</p>
      <Rating
          name="half-rating"
          defaultValue={0}
          precision={0.5}
          value={lunchvalue}
          onChange={(event, newlunchValue) => {
          setLunchValue(newlunchValue);
          }}
      />
      <p>ディナー</p>
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
      <Button onClick={(e) => {handleClose(); Review(e);}}>決定</Button>
      </DialogActions>
    </Dialog>
    </div>
  );
}

export default PopUp;