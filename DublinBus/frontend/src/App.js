import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Header from "./Components/Header";
import Footer from "./Components/Footer";
import SearchByStop from "./Components/SearchByStop";
import SearchbyDestination from "./Components/SearchbyDestination";
import HomePage from "./Components/HomePage";
import SearchByRoute from "./Components/SearchByRoute";
import NoPathToRender_ThenThisPage from "./Components/NoPathToRender_ThenThisPage";
import ResultPage_Stop_Route from "./Components/ResultPage_Stop_Route";
import ResultPageDestination from "./Components/ResultPageDestination";
import Map from "./Components/Map";


class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Header />
          <div className="container-fluid position-relative">
            <Switch>
              <Route path="/" exact={true} component={HomePage} />
              <Route
                path="/SearchByDestination"
                component={SearchbyDestination}
              />
              <Route path="/SearchByRoute" component={SearchByRoute} />
              <Route path="/SearchByStop" component={SearchByStop} />
              <Route
                path="/ResultPage_Stop_Route/:stopnumber"
                component={ResultPage_Stop_Route}
              />

              <Route
                path="/ResultPageDestination/:startCoordinates/:destinationCoordinates/:startDateToBackEnd/:startTimeToBackEnd"
                component={ResultPageDestination}
              />
              {/*<Route component={NoPathToRender_ThenThisPage} />*/}
            </Switch>
          </div>
          <Footer />
        </div>
      </Router>
    );
  }
}

export default App;
