import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Landing from "./pages/landing";
import About from "./pages/about";
import Works from "./pages/works";
import Tool from "./pages/tool";
import Progress from "./pages/progress";
import Graph from "./pages/graph";

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
        <Route exact path="/data-upload">
          <Tool />
        </Route>
        <Route exact path="/loading">
          <Progress />
        </Route>
        <Route exact path="/graph-:filename">
          <Graph />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
