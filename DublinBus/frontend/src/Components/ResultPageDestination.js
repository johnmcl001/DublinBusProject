import React, { Component } from "react";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import ResultPageButton from "./ResultPageButton";
import "../Static/StyleSheet/ResultPageDestination.css";
import DataProvider from "./DataProvider";
import Table from "./Table";


//This Component is the Result page of Search By Destination
class ResultPageDestination extends Component {
  render() {
    return (
      <div
        className="EntireBox  container col-md-12  position-absolute bg-light"
        id="EntireBox_ResultDestination"
      >
        <div className="container ">
          <AppViewHeader SearchState={"Real time Information"} />
          <AppViewFavourAndLogin />
        </div>
        <div className="row ">
          <div className="col-8 resultLabel  ">
            <h4>To 'To be Change'</h4>
          </div>
        </div>
        <div className="container border border-primary">
          <div className="container ResultPageDestination  ">
            <ul className="nav nav-pills mb-3" id="pills-tab" role="tablist">
              <li className="nav-item">
                <a
                  className="nav-link active"
                  id="pills-home-tab"
                  data-toggle="pill"
                  href="#pills-home"
                  role="tab"
                  aria-controls="pills-home"
                  aria-selected="true"
                >
                  Option 1
                </a>
              </li>
              <li className="nav-item">
                <a
                  className="nav-link"
                  id="pills-profile-tab"
                  data-toggle="pill"
                  href="#pills-profile"
                  role="tab"
                  aria-controls="pills-profile"
                  aria-selected="false"
                >
                  Option 2
                </a>
              </li>
              <li className="nav-item">
                <a
                  className="nav-link"
                  id="pills-contact-tab"
                  data-toggle="pill"
                  href="#pills-contact"
                  role="tab"
                  aria-controls="pills-contact"
                  aria-selected="false"
                >
                  Option 3
                </a>
              </li>
            </ul>
            <div className="tab-content" id="pills-tabContent">
              <div
                className="tab-pane fade show active"
                id="pills-home"
                role="tabpanel"
                aria-labelledby="pills-home-tab"
              >
      <DataProvider
        endpoint="destination"
        startpoint={this.props.match.params.startCoordinates}
        destination={this.props.match.params.startCoordinates}
        time={this.props.match.params.startTimeToBackEnd}
        date={this.props.match.params.startDateToBackEnd}
        render={data => <Table data={data} />}
      />
              </div>
              <div
                className="tab-pane fade"
                id="pills-profile"
                role="tabpanel"
                aria-labelledby="pills-profile-tab"
              >
                ...
              </div>
              <div
                className="tab-pane fade"
                id="pills-contact"
                role="tabpanel"
                aria-labelledby="pills-contact-tab"
              >
                ...
              </div>
            </div>
          </div>
        </div>
        <ResultPageButton />
      </div>
    );
  }
}


export default ResultPageDestination;
