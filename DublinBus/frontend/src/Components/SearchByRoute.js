import React, { Component } from "react";
import "../Static/StyleSheet/SearchByRoute.css";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import { Link } from "react-router-dom";
import Autocomplete from "./Autocomplete";
import DropDown from "./DropDown";

/*
  SQL Query Template
  select distinct s.stopID_short, s.stop_name
  from stops s, stop_times st, trips t, routes r, calendar c
  where s.stop_id = st.stop_id and
  st.trip_id = t.trip_id and
  t.route_id = r.route_id and
  t.service_id = c.service_id and
  r.route_short_name = <route> and
  st.stop_headsign = <direction> and
  c.<day> = 1;
  Example route: 46a
  Example direction: Phoenix Pk
  Example day: monday
*/

var routeList = require("../Json/routes_directions.json");

//This Component is Search by Route at the mobile view ports
class SearchByRoute extends Component {
  constructor(props) {
    super(props);
    this.state = {
      SearchState: "Search By Route",
      routeNumber: "Route Number",
      routeAutocomplete: Object.keys(routeList),
      direction: "Direction",
      directionAutocomplete: [],
      stopNumber: "Stop",
      stopsAutocomplete: ""
    };
    this.updateRoute = this.updateRoute.bind(this);
    this.updateDirection = this.updateDirection.bind(this);
    this.updateStop = this.updateStop.bind(this);
    this.updateDirectionAutocomplete = this.updateDirectionAutocomplete.bind(
      this
    );
    this.updateStopAutocomplete = this.updateStopAutocomplete.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  updateRoute(e) {
    this.setState({ routeNumber: e });
  }

  updateDirection(e) {
    this.setState({ direction: e });
  }

  updateStop(e) {
    this.setState({ stopNumber: e });
  }

  updateDirectionAutocomplete(e) {
    this.setState({ directionAutocomplete: routeList[e] });
  }

  updateStopAutocomplete(e) {
    this.setState({ stopNumber: e });
  }

  handleSubmit(e) {
    alert(this.state.direction);
    e.preventDefault();
  }

  render() {
    return (
      <div
        className="EntireBox SearchByRoute container col-md-12  position-absolute"
        id="EntireBox_SearchRoute"
      >
        <div className="container SearchByRouteBox bg-light">
          <AppViewHeader SearchState={this.state.SearchState} />
          <AppViewFavourAndLogin />
          <div id="formColor">
            <form onSubmit={this.handleSubmit}>
              <div className="row row_first"></div>
              <div className="row rowSpace ">
                <div className="col-5 RouteNumber  ">
                  <label htmlFor="fname"> Route Number :</label>
                </div>
                <div className="col-7 RouteNumber inputBox">
                  <Autocomplete
                    suggestions={this.state.routeAutocomplete}
                    updateState={this.updateRoute}
                    updateAutocomplete={this.updateDirectionAutocomplete}
                  />
                </div>
              </div>

              <div className="row rowSpace">
                <div className="col-5  ">
                  <label htmlFor="Towards">Towards :</label>
                </div>
                <div className="col-7 inputBox">
                  <DropDown
                    suggestions={this.state.directionAutocomplete}
                    updateState={this.updateDirection}
                    updateAutocomplete={this.updateStopAutocomplete}
                  />
                </div>
              </div>

              <div className="row rowSpace ">
                <div className="col-5 ">
                  <label htmlFor="fname"> Departure :</label>
                </div>
                <div className="col-7  inputBox">
                  <Autocomplete
                    suggestions={this.state.stopsAutocomplete}
                    updateState={this.updateStop}
                  />
                </div>
              </div>
              <input type="submit" value="Submit" />
            </form>
          </div>

          <Link to={"/ResultPage_Stop_Route"}>
            <button
              type="button"
              className="btn btn-warning col-7"
              id="SubmitButton"
            >
              Submit
            </button>
          </Link>
        </div>
      </div>
    );
  }
}

export default SearchByRoute;
