import React, { Component } from "react";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import "../Static/StyleSheet/StyleSearchByStop.css";
import { Link } from "react-router-dom";
import ResultPage_Stop_Route from "./ResultPage_Stop_Route";
import AppViewHeader from "./AppViewHeader";
import Autocomplete from "./Autocomplete";
import WarningAlert from "./WarningAlert";
import "bootstrap";
import * as $ from "jquery";
import { createBrowserHistory } from "history";

const history = createBrowserHistory();

var busList = require("../Json/frontEndBusInfo.json");

//This Component is Search by Stop at the mobile view ports
class SearchByStop extends Component {
  constructor(props) {
    super(props);
    this.state = {
      stopNumber: "Stop Number",
      stopsautocomplete: Object.keys(busList)
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.updateStop = this.updateStop.bind(this);
  }

  updateStop(e) {
    this.setState({ stopNumber: Number(e) });
  }

  handleSubmit() {
    // event.preventDefault();
  }

  ensureFill() {
    if (Number.isInteger(this.state.stopNumber) && this.state.stopNumber != 0) {
      this.props.history.push(
        `/ResultPage_Stop_Route/${this.state.stopNumber}/null`
      );
    } else {
      //This is used to activate the alert box

      (function($) {
        $("#SearchByStop").modal("toggle");
      })(jQuery);
    }
  }

  render() {
    return (
      <div
        className="EntireBox SearchByStop container position-absolute col-md-12 bg-light"
        id="EntireBox_SearchStop"
      >
        <AppViewHeader
          SearchState="Search by Stop Number"
          Return="toHomePage"
        />
        <AppViewFavourAndLogin />
        <div className="col-12" id="formColor">
          <form id="SearchByStopForm" onSubmit={this.handleSubmit}>
            <label htmlFor="fname">Stop Number : </label>
            {/*Pass updateStop function so that child updates parent*/}
            <Autocomplete
              suggestions={this.state.stopsautocomplete}
              updateState={this.updateStop}
              updateAutocomplete={this.handleSubmit}
            />
          </form>
        </div>

        <div className="col-8  bottomClass">
          {/*<Link to={`/ResultPage_Stop_Route/${this.state.stopNumber}/null`}>*/}
          <button
            type="button"
            className="btn btn-warning "
            id="SubmitButton"
            onClick={this.ensureFill.bind(this)}
          >
            Submit
          </button>
          {/*</Link>*/}
        </div>

        <WarningAlert
          color={"#F65314"}
          id={"SearchByStop"}
          title={"Warning"}
          content={"Please enter your topnumber"}
        />
      </div>
    );
  }
}

export default SearchByStop;
