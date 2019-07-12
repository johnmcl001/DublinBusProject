import React, { Component } from "react";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import "../Static/StyleSheet/StyleSearchByStop.css";
import { Link } from "react-router-dom";
import ResultPage_Stop_Route from "./ResultPage_Stop_Route";
import AppViewHeader from "./AppViewHeader";
import Autocomplete from "./Autocomplete";

var busList = require("../Json/frontEndBusInfo.json");

//This Component is Search by Stop at the mobile view ports
class SearchByStop extends Component {
  constructor(props) {
    super(props);
    this.state = {
      stopnumber: "Stop Number",
      stopsautocomplete: Object.keys(busList)
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.updateStop = this.updateStop.bind(this);
  }

  updateStop(e) {
    this.setState({ stopnumber: e });
  }

  handleSubmit(event) {
    event.preventDefault();
  }

  render() {
    return (
      <div
        className="EntireBox SearchByStop container position-absolute col-md-12 bg-light"
        id="EntireBox_SearchStop"
      >
        <AppViewHeader SearchState="Search by Stop Number" />
        <AppViewFavourAndLogin />
        <div className="col-12" id="formColor">
          <form id="SearchByStopForm" onSubmit={this.handleSubmit}>
            <label htmlFor="fname">Stop Number : </label>
            {/*Pass updateStop function so that child updates parent*/}
            <Autocomplete
              suggestions={this.state.stopsautocomplete}
              onUpdateStop={this.updateStop}
            />
          </form>
        </div>
        <Link to={`/ResultPage_Stop_Route/${this.state.stopnumber}`}>
          <button
            type="button"
            className="btn btn-warning col-7"
            id="SubmitButton"
          >
            Submit
          </button>
        </Link>
      </div>
    );
  }
}

export default SearchByStop;
