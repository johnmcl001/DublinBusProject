import React, {Component} from "react";
import {BrowserRouter as Router, Switch, Route} from "react-router-dom";
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
import "./App.css";

const polyLine = [];

class App extends Component {
    constructor() {
        super();
        this.state = {
            polyline: [],
            markers: []
        };
        this.updateMap = this.updateMap.bind(this);
    }

    updateMap = newMapInfo => {
        console.log(newMapInfo);
        this.setState({
            polyline: newMapInfo[0].hasOwnProperty("map")
                ? newMapInfo[0].map.polyline
                : []
        });
        this.setState({
            markers: newMapInfo[0].hasOwnProperty("map")
                ? newMapInfo[0].map.markers
                : []
        });
    };

    render() {
        return (
            <Router>

                <div className="App">
                    <div className="container-fluid position-relative appContainer">
                        <Map polyline={this.state.polyline} markers={this.state.markers}/>

                        <Switch>
                            <Route path="/" exact={true} component={HomePage}/>
                            <Route
                                path="/SearchByDestination"
                                render={({updateMap, match, history}) => (
                                    <SearchbyDestination
                                        updateMap={this.updateMap}
                                        match={match}
                                        history={history}
                                        polyline={this.state.polyline}
                                        markers={this.state.markers}
                                    />
                                )}
                            />
                            <Route path="/SearchByRoute" component={SearchByRoute}/>
                            <Route path="/SearchByStop" component={SearchByStop}/>
                            <Route path="/JourneyPlanner" component={JourneyPlanner}/>
                            <Route
                                path="/ResultPage_Stop_Route/:stopnumber/:route"
                                render={({updateMap, match}) => (
                                    <ResultPage_Stop_Route
                                        updateMap={this.updateMap}
                                        match={match}
                                        polyline={this.state.polyline}
                                        markers={this.state.markers}
                                    />
                                )}
                            />
                            <Route
                                path="/JourneyPlannerResultPage/:startLat/:startLon/:startDateToBackend/:startTimeToBackend/:PickedTouristAttraction/:home"
                                render={({updateMap, match}) => (
                                    <JourneyPlannerResultPage
                                        updateMap={this.updateMap}
                                        match={match}
                                        polyline={this.state.polyline}
                                        markers={this.state.markers}
                                    />
                                )}
                            />

                            <Route
                                path="/ResultPageDestination/:startLat/:startLon/:destinationLat/:destinationLon/:startDateToBackEnd/:startTimeToBackEnd/:start/:end"
                                render={({updateMap, match}) => (
                                    <ResultPageDestination
                                        updateMap={this.updateMap}
                                        match={match}
                                        polyline={this.state.polyline}
                                        markers={this.state.markers}
                                    />
                                )}
                            />
                            {/*<Route component={NoPathToRender_ThenThisPage} />*/}
                        </Switch>
                    </div>
                    <Footer/>
                </div>
            </Router>
        );
    }
}

export default App;
