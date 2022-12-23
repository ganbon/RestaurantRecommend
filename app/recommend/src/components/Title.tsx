import Typography from '@mui/material/Typography';
type TitleProps = {
    title: string
  }
const Title = (props:TitleProps) =>{
    return (
        <Typography variant="h2" textAlign="center">{props.title}</Typography>
    );
}

export default Title