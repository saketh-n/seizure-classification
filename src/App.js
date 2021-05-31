import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Landing from "./pages/landing";
import About from "./pages/about";
import Works from "./pages/works";

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/">
          <Landing />
        </Route>
        <Route exact path="/about">
          <About />
        </Route>
        <Route exact path="/how-it-works">
          <Works />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
