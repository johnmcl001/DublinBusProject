import React, { Component } from "react";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import ResultPageButton from "./SlideShowMobileMap";
import "../Static/StyleSheet/ResultPageDestination.css";
import JourneyPlanner_Table from "./JourneyPlanner_Table";
import DataProvider from "./DataProvider";
import JouneryPlanner_ToVisitPiont from "./JourneyPlanner";
import JourneyPlannerResultsDisplay from "./JourneyPlannerResultsDisplay";

//This Component is the Result page of Search By Destination
class JourneyPlaner_ResultPage extends Component {
  render() {
    const color = ["#F65314", "#7CBB00", "#00A1F1", "#FFBB00", "#146EB4"];
    return (
      <div
        className="EntireBox  container col-md-12  position-absolute bg-light"
        id="EntireBox_ResultDestination"
      >
        <div className="container ">
          <AppViewHeader SearchState={"Real time Information"} />
          <AppViewFavourAndLogin />
        </div>


          <DataProvider
            endpoint="touristplanner"
            updateMap={this.props.updateMap}
            attractions='["Trinity College Dublin","The Spire","Guinness Storehouse"]'
            home='Westin'
            render={data => <JourneyPlannerResultsDisplay data={data} />}
          />



        <ResultPageButton />
      </div>
    );
  }
}

export default JourneyPlaner_ResultPage;
