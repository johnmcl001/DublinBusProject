import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Header from "./Components/Header";
import Footer from "./Components/Footer";
import SearchByStop from "./Components/SearchByStop";
import SearchbyDestination from "./Components/SearchbyDestination";
import HomePage from "./Components/HomePage";
import SearchByRoute from "./Components/SearchByRoute";
import JourneyPlanner from "./Components/JourneyPlanner";
import NoPathToRender_ThenThisPage from "./Components/NoPathToRender_ThenThisPage";
import ResultPage_Stop_Route from "./Components/ResultPage_Stop_Route";
import ResultPageDestination from "./Components/ResultPageDestination";
import JourneyPlannerResultPage from "./Components/JourneyPlaner_ResultPage";
import Map from "./Components/Map";
import decodePolyline from "decode-google-map-polyline";
import MobileMap from "./Components/MobileMap";

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Header />
          <div className="container-fluid position-relative">
            <Map />
            <Switch>
              <Route path="/" exact={true} component={HomePage} />
              <Route
                path="/SearchByDestination"
                component={SearchbyDestination}
              />
              <Route path="/SearchByRoute" component={SearchByRoute} />
              <Route path="/SearchByStop" component={SearchByStop} />
              <Route path="/JourneyPlanner" component={JourneyPlanner} />
              <Route
                path="/ResultPage_Stop_Route/:stopnumber"
                component={ResultPage_Stop_Route}
              />
              <Route
                path="/JourneyPlannerResultPage/"
                component={JourneyPlannerResultPage}
              />

              <Route
                path="/ResultPageDestination/:startLat/:startLon/:destinationLat/:destinationLon/:startDateToBackEnd/:startTimeToBackEnd/:start/:end"
                render={({ updateMap, match }) => (
                  <ResultPageDestination
                    updateMap={this.updateMap}
                    match={match}
                  />
                )}
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
