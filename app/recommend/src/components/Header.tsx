import Typography from '@mui/material/Typography';
import AppBar from '@mui/material/AppBar';
import Button from '@mui/material/Button';
import Toolbar from '@mui/material/Toolbar';   

type TitleProps = {
    title: string
}

const Header = (props:TitleProps) =>{
    return (
        <AppBar position="static" color="primary">
        <Toolbar>
        <Typography variant="h5" textAlign="center">{props.title}</Typography>
        <div style={{ flexGrow: 1 }}></div>
        <Button href="/" color="inherit">トップ</Button>
        <Button href="/search" color="inherit">検索</Button>
        <Button href="/new" color="inherit">あなたへのおすすめ</Button>
        <Button href="/history" color="inherit">履歴</Button>
        </Toolbar>
      </AppBar>
    );
}

export default Header