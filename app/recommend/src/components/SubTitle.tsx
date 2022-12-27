import Typography from '@mui/material/Typography';
type TitleProps = {
    title: string
  }
const SubTitle = (props:TitleProps) =>{
    return (
        <Typography variant="h4" textAlign="center">{props.title}</Typography>
    );
}

export default SubTitle