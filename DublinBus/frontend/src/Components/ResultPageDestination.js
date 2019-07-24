import React, { Component } from "react";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import ResultPageButton from "./ResultPageButton";
import "../Static/StyleSheet/ResultPageDestination.css";
import DataProvider from "./DataProvider";
import Table from "./Table";
import { FaWalking, FaLevelDownAlt, FaMapMarkerAlt } from "react-icons/fa";
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
        <div>
          <DataProvider
            endpoint="destination"
            updateMap={this.props.updateMap}
            startLat={this.props.match.params.startLat}
            startLon={this.props.match.params.startLon}
            destinationLat={this.props.match.params.destinationLat}
            destinationLon={this.props.match.params.destinationLon}
            time={this.props.match.params.startTimeToBackEnd}
            date={this.props.match.params.startDateToBackEnd}
            render={data => <Table data={data} />}
          />
        </div>
        <ResultPageButton />
      </div>
    );
  }
}
export default ResultPageDestination;
