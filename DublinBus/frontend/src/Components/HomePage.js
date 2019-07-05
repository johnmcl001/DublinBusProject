import React, { Component } from "react";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import { Link, BrowserRouter } from "react-router-dom";
import "../Static/StyleSheet/HomePage.css";

class HomePage extends Component {
  render() {
    return (
      <BrowserRouter>
        <div className="EntireBox HomePage container col-md-12  position-absolute bg-light">
          <div className="row  WeatherWidget border border-danger ">
            <div className="container " id="WeatherWidget">
              <a
                className="weatherwidget-io"
                href="https://forecast7.com/en/53d35n6d26/dublin/"
                data-label_1="DUBLIN"
                data-label_2="WEATHER"
                data-font="Arial Black"
                data-icons="Climacons Animated"
                data-mode="Current"
                data-days="3"
                data-theme="original"
              >
                DUBLIN WEATHER
              </a>
            </div>
          </div>
          <div className="container bg-light">
            <AppViewFavourAndLogin />
            <div className="container  bg-light HomePageInner">
              <div className="row border border-danger ">
                <Link to={"/SearchByStop"}>Search By Stop</Link>
              </div>
              <div className="row border border-danger ">
                <button type="button" className="btn btn-success">
                  Search By Route
                </button>
              </div>
              <div className="row border border-danger ">
                <button type="button" className="btn btn-success">
                  Search By Destination
                </button>
              </div>
            </div>
          </div>
        </div>
      </BrowserRouter>
    );
  }
}

export default HomePage;
