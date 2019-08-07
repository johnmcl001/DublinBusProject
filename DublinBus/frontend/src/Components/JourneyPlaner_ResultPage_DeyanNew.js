import React, {Component} from "react";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import ResultPageButton from "./SlideShowMobileMap";
import "../Static/StyleSheet/ResultPageDestination.css";
import JourneyPlanner_Table from "./JourneyPlanner_Table"
import { Accordion} from 'react-bootstrap';

import DataProvider from "./DataProvider";

//This Component is the Result page of Search By Destination
class JourneyPlaner_ResultPage extends Component {

    render() {
        const color = ['#F65314', '#7CBB00', '#00A1F1', '#FFBB00', '#146EB4','#E32934','#004883']
        return (

            <div
                className="EntireBox  container col-md-12  position-absolute bg-light"
                id="EntireBox_ResultDestination"
            >
                <div className="container ">
                    <AppViewHeader SearchState={"Real time Information"}/>
                    <AppViewFavourAndLogin/>
                </div>


                <Accordion>

                              {/*<DataProvider*/}
            {/*endpoint="destination"*/}
            {/*updateMap={this.props.updateMap}*/}
            {/*startLat={this.props.match.params.startLat}*/}
            {/*startLon={this.props.match.params.startLon}*/}
            {/*destinationLat={this.props.match.params.destinationLat}*/}
            {/*destinationLon={this.props.match.params.destinationLon}*/}
            {/*time={this.props.match.params.startTimeToBackEnd}*/}
            {/*date={this.props.match.params.startDateToBackEnd}*/}
            {/*render={data => <Table data={data} />}*/}
          {/*/>*/}

                    <JourneyPlanner_Table number={1} buttonID={`ResultPageButton_${1}`} cardID={`AttractionStop_${1}`}
                                          color={color[1]}/>


                    <JourneyPlanner_Table number={2} buttonID={`ResultPageButton_${2}`} cardID={`AttractionStop_${2}`}
                                          color={color[2]}/>


                </Accordion>


                <ResultPageButton/>
            </div>
        );
    }
}

export default JourneyPlaner_ResultPage;
