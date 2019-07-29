import React, { Component } from "react";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import ResultPageButton from "./SlideShowMobileMap";
import "../Static/StyleSheet/ResultPage_Stop_Route.css";
import DataProvider from "./DataProvider";
import ResultTable_StopRoute from "./ResultTable_StopRoute";

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

            <DataProvider
              endpoint="stop"
              stopnumber={this.props.match.params.stopnumber}
              render={data => <ResultTable_StopRoute data={data} />}
            />
          </form>
        </div>
        <ResultPageButton />
      </div>
    );
  }
}

export default ResultPage_Stop_Route;
