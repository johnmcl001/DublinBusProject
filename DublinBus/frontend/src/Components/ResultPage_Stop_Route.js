import React, { Component } from "react";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import ResultPageButton from "./ResultPageButton";
import "../Static/StyleSheet/ResultPage_Stop_Route.css";
import DataProvider from "./DataProvider";
import Table from "./Table";

//This is Result Page Component for Search for Stop and Route
class ResultPage_Stop_Route extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div
        className="EntireBox  container col-md-12  position-absolute bg-light"
        id="EntireBox_ResultPageStopRoute"
      >
        <div className="container ">
          <AppViewHeader SearchState={"Real time Information"} />
          <AppViewFavourAndLogin />
        </div>
        <div className="container resultPageStop_Route ">
          <div className="row ">
            <div className="col-8 resultLabel  ">
              <h4>Stop {this.props.match.params.stopnumber}</h4>
            </div>
          </div>

          <form className="border border-primary ">
            <div className="row busLabels ">
              <div className="col-4 ">
                <p>Bus</p>
              </div>
              <div className="col-8  ">
                <p id="ArrivalLabel">Estimate arrival </p>
              </div>
            </div>

            <div className="row resultRows">
              <div className="col-4 busNumber">
                <p>39A</p>
              </div>
              <div className="col-6 busArrivalTime ">
                <p>6 mins</p>
              </div>
            </div>
            <div className="row resultRows">
              <div className="col-4 busNumber">
                <p>39A</p>
              </div>
              <div className="col-6 busArrivalTime ">
                <p>16 mins</p>
              </div>
            </div>

            <div className="row resultRows" id="resultRowsLastRaw">
              <div className="col-4 busNumber">
                <p>39A</p>
              </div>
              <div className="col-6 busArrivalTime ">
                <p>21 mins</p>
              </div>
            </div>
          </form>
          <DataProvider
            endpoint="stop"
            stopnumber={this.props.match.params.stopnumber}
            render={data => <Table data={data} />}
          />
        </div>
        <ResultPageButton />
      </div>
    );
  }
}

export default ResultPage_Stop_Route;
