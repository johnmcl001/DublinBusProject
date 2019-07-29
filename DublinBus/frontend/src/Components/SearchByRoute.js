import React, { Component } from "react";
import "../Static/StyleSheet/SearchByRoute.css";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import { Link } from "react-router-dom";
import Autocomplete from "./Autocomplete";
import DropDown from "./DropDown";
import axios from "axios";

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
      stopsAutocomplete: []
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
    this.setState({ stopNumber: e.substring(0, e.indexOf(","))});
  }

  updateDirectionAutocomplete(e) {
    this.setState({ directionAutocomplete: routeList[e] });
  }

  updateStopAutocomplete(e) {
    this.state.stopsAutocomplete = axios({
      method: "get",
      url: "http://localhost:8000/api/stopsautocomplete/",
      params: {
        route: this.state.routeNumber,
        direction: this.state.direction
      }
    })
      .then(response => {
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.data;
      })
      .then(data => this.setState({ stopsAutocomplete: data, loaded: true }));
  }

  handleSubmit(e) {
    {
      /*alert(new Date().toLocaleString('en-us', {  weekday: 'long' }).toLowerCase());*/
    }
    e.preventDefault();
  }

  render() {
    return (
      <div
        className="EntireBox SearchByRoute container col-md-12  position-absolute"
        id="EntireBox_SearchRoute"
      >
        <div className="container SearchByRouteBox bg-light">
          <AppViewHeader
            SearchState={this.state.SearchState}
            Return="toHomePage"
          />
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
                <div className="col-7 inputBox  ">
                  <DropDown
                    suggestions={this.state.directionAutocomplete}
                    updateState={this.updateDirection}
                    updateAutocomplete={this.updateStopAutocomplete}
                  />
                </div>
              </div>

              <div className="row rowSpace ">
                <div className="col-5 ">
                  <label htmlFor="fname"> Departure Stop:</label>
                </div>
                <div className="col-7  inputBox">
                  <Autocomplete
                    suggestions={this.state.stopsAutocomplete}
                    updateState={this.updateStop}
                    updateAutocomplete={this.handleSubmit}
                  />
                </div>
              </div>
            </form>
          </div>
        <div className="col-8  bottomClass">
          <Link to={`/ResultPage_Stop_Route/${this.state.stopNumber}/${this.state.routeNumber}`}>
            <button
              type="button"
              className="btn btn-warning "
              id="SubmitButton"
            >
              Submit
            </button>
          </Link>
        </div>
        </div>
      </div>
    );
  }
}

export default SearchByRoute;
