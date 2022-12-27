import Top from "./components/Top"
import SaerchPage from "./components/Search"
import Recommend from "./components/Recommend";
import './App.css';
import { BrowserRouter, Switch, Route } from "react-router-dom";

function App() {
  return (
    <div className="app">
      <BrowserRouter> 
        <Switch>
          <Route  exact path="/">
            <Top />
          </Route>
          <Route path="/search">
            <SaerchPage />
          </Route>
        <Route path="/new">
            <Recommend />
          </Route>
          <Route path="/popular">
            <Recommend />
          </Route>
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
