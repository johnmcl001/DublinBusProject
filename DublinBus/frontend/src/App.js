import React, {Component, setState } from "react";
import {BrowserRouter as Router, Switch, Route} from "react-router-dom";
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
import MapContext from "./Components/MapContext";
import decodePolyline from "decode-google-map-polyline";

const polyLine = [];

class App extends Component {
    constructor(){
        super()
        this.state = {
            polyline: []
        }
        this.updatePolyline = this.updatePolyline.bind(this);
    }

    updatePolyline = (newline) => {
        this.setState({polyline: newline});


    }
    render() {
        return (
            <Router>
                <div className="App">
                        <Header/>
                    <div className="container-fluid position-relative">
                        <Map path={this.state.polyline} />

                        <Switch>
                            <Route path="/" exact={true} component={HomePage}/>
                            <Route
                                path="/SearchByDestination"
                                component={SearchbyDestination}
                            />
                            <Route path="/SearchByRoute" component={SearchByRoute}/>
                            <Route
                            path="/SearchByStop"
                            component={SearchByStop}
                            />
                            <Route
                                path="/ResultPage_Stop_Route/:stopnumber"
                                component={ResultPage_Stop_Route}
                            />

                            <Route
                                path="/ResultPageDestination/:startCoordinates/:destinationCoordinates/:startDateToBackEnd/:startTimeToBackEnd"
                                render={(updatePolyline) => (
                                <ResultPageDestination updatePolyline={this.updatePolyline} />
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
