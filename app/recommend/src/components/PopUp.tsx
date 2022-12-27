import React, { useState } from 'react'
import { Rating,Dialog,Button } from '@mui/material';
import DialogActions from '@mui/material/DialogActions';
import DialogTitle from '@mui/material/DialogTitle';




const PopUp = (props:any) => {
  const [open, setOpen] = React.useState(false);
  const [value, setValue] = React.useState<number | null>(0);
  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };
  return (
    <div>
    <Button variant="outlined" onClick={handleClickOpen}>
          ブックマーク
      </Button>
      <Dialog onClose={handleClose} open={open}>
          <DialogTitle>レビュー</DialogTitle>
          <p>ランチ</p>
          <Rating
              name="half-rating"
              defaultValue={0}
              precision={0.5}
              value={value}
              onChange={(event, newlunchValue) => {
              setValue(newlunchValue);
              }}
          />
          <p>ディナー</p>
          <Rating
              name="half-rating"
              value={value}
              defaultValue={0}
              precision={0.5}
              onChange={(event, newdinnerValue) => {
              setValue(newdinnerValue);
              }}
          />
          <DialogActions>
          <Button onClick={handleClose}>閉じる</Button>
          <Button onClick={() => {handleClose(); props.Review();}}>決定</Button>
          </DialogActions>
    </Dialog>
    </div>
  );
}

export default PopUp;