import React, { Component } from "react";
import { Link } from "react-router-dom";
import "../Static/StyleSheet/SearchbyDestination.css";
import "../Static/StyleSheet/JourneyPlanner.css";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import YourLocationOrSearch from "./YourLocationOrSearch";
import JouneryPlanner_ToVisitPiont from "./JouneryPlanner_ToVisitPiont";
import JourneyPanner_SlideShow_List_DublinAttaction from "./JourneyPanner_SlideShow_List_DublinAttaction";
import Cards from "./JourneyPlanner_Card";

// npm install react-datepicker --save
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import Imgx from "../Static/img/img1.jpg";

//This Component is Search by Destination at the mobile view ports
class JourneyPlanner extends Component {
  constructor(props) {
    super(props);
    this.state = {
      initial_Date: null,
      initial_Time: null,

      startDateToBackEnd: null,
      startTimeToBackEnd: null,

      //Location Co-Ordinate start Here
      currentLocation_lat: null,
      currentLocation_long: null,

      startLocation_lat: null,
      startLocation_long: null
    };
    this.handleChangeDate = this.handleChangeDate.bind(this);
    this.handleChangeTime = this.handleChangeTime.bind(this);

    this.updateCurrentPosition = this.updateCurrentPosition.bind(this);

    this.setPosition = this.setPosition.bind(this);
    this.getLocation = this.getLocation.bind(this);
  }

  updateCurrentPosition(e) {
    this.setState({
      startLocation_lat: e.latitude,
      startLocation_long: e.longitude
    });
  }

  handleChangeDate(date) {
    //set date
    this.setState({
      initial_Date: date,
      startDateToBackEnd:
        date.getDate() + "-" + (date.getMonth() + 1) + "-" + date.getFullYear()
    });
  }

  handleChangeTime(Time) {
    //set time
    this.setState({
      initial_Time: Time,
      startTimeToBackEnd: Time.getHours() + ":" + Time.getMinutes()
    });
  }

  //This is Geolocation ask for current location
  setPosition(position) {
    this.setState({
      currentLocation_lat: position.coords.latitude,
      currentLocation_long: position.coords.longitude
    });
  }

  //Ask for permission to obtain current locations
  getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(this.setPosition);
    }
  }

  componentDidMount() {
    this.getLocation();
  }

  render() {
    console.log(this.state.currentLocation_lat);

    return (
      <div>
        <div className="EntireBox  SearchByDestinationBox JoureyPlaner bg-light container col-md-12  position-absolute  ">
          {/*<div className='container '>*/}
          <AppViewHeader SearchState={"Journey Planner"} Return="toHomePage" />
          <AppViewFavourAndLogin />
          <div id="formColor">
            <form>
              <div className="container  SearchByDestinationForm">
                <div className="row  JourneyPlannerRowSecond">
                  <div className="col-12 JourneyPlanerAddressLabel ">
                    <label> Start Point:</label>
                  </div>

                  <div className="col-10 JourneyPlanerInput ">
                    <YourLocationOrSearch
                      onUpdatePosition={this.updateCurrentPosition}
                    />
                  </div>
                </div>

                <div className="row JoureyPlanerTimeLabel ">
                  <div className="col-6">
                    <label> Time:</label>
                  </div>
                  <div className="col-6">
                    <label> Date:</label>
                  </div>
                </div>

                <div className="row row_fifth ">
                  <div className="col-6  ">
                    <DatePicker
                      selected={this.state.initial_Date}
                      onChange={this.handleChangeDate}
                      placeholderText="Today"
                    />
                  </div>
                  <div className="col-6 ">
                    <DatePicker
                      selected={this.state.initial_Time}
                      onChange={this.handleChangeTime}
                      showTimeSelect
                      showTimeSelectOnly
                      timeIntervals={15}
                      dateFormat="h:mm aa"
                      timeCaption="Time"
                      placeholderText="Now"
                    />
                  </div>
                </div>

                {/*List of Tourist To visit Location  */}
                <div className="col-12 listDestination_label  ">
                  <label> Selected Attraction:</label>
                </div>
                <div className="accordion" id="accordionExample">
                  <div className="row listDestination border border-white ">
                    <JouneryPlanner_ToVisitPiont
                      buttonID="button_1"
                      cardID="attraction_1"
                    />
                    <JouneryPlanner_ToVisitPiont
                      buttonID="button_2"
                      cardID="attraction_2"
                    />
                    <JouneryPlanner_ToVisitPiont
                      buttonID="button_3"
                      cardID="attraction_3"
                    />
                    <JouneryPlanner_ToVisitPiont
                      buttonID="button_4"
                      cardID="attraction_4"
                    />
                    <JouneryPlanner_ToVisitPiont
                      buttonID="button_5"
                      cardID="attraction_5"
                    />
                  </div>
                </div>
                <div>
                  <JourneyPanner_SlideShow_List_DublinAttaction />
                </div>
              </div>
            </form>
          </div>

          <div className="row NotificationButton border border-secondary">
            <p>NotificationButton locate here</p>
          </div>
          <Link to={`/JourneyPlannerResultPage/`}>
            <button
              type="button"
              className="btn btn-warning col-7"
              id="SubmitButton"
            >
              Submit
            </button>

            <button type="button" className="btn btn-danger">
              Create an Event
            </button>
          </Link>

          {/*</div>*/}
        </div>

        <div className="ListofAllAttractions d-none d-lg-block">
          <Cards />
          <Cards />
        </div>
      </div>
    );
  }
}

export default JourneyPlanner;
