import Top from "./components/Top"
import SaerchPage from "./components/Search"
import Recommend from "./components/Recommend";
import History from "./components/History";
import './App.css';
import { BrowserRouter, Switch, Route } from "react-router-dom";

function App() {
  return (
    <div className="app">
      <BrowserRouter> 
        <Switch>
          <Route  exact path="/" component={Top}/>
          <Route path="/search"component={SaerchPage}/>
        <Route path="/new"component={Recommend}/>
          <Route path="/history"component={History}/>
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
