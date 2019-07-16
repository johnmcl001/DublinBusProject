import React, { Component } from "react";
import { Link } from "react-router-dom";
import "../Static/StyleSheet/SearchbyDestination.css";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";

import GoogleAddressSearch from "./GoogleAddressSearch";

// npm i react-moment --save

// npm install react-datepicker --save
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";

//This Component is Search by Destination at the mobile view ports
class SearchbyDestination extends Component {
  constructor(props) {
    super(props);
    this.state = {
      initial_Date: null,
      initial_Time: null,

      startDateToBackEnd: null,
      startTimeToBackEnd: null,

      currentLocation: null,
      startLocation: true,

      startCoordinates: null,
      destinationCoordinates: null
    };
    this.handleChangeDate = this.handleChangeDate.bind(this);
    this.handleChangeTime = this.handleChangeTime.bind(this);

    this.updateCurrentPosition = this.updateCurrentPosition.bind(this);
    this.setDestination = this.setDestination.bind(this);

    this.setPosition = this.setPosition.bind(this);
    this.getLocation = this.getLocation.bind(this);
  }

  updateCurrentPosition(e) {
    this.setState({
      startCoordinates: e
    });
  }

  setDestination(e) {
    //set Co-ordinate for destination box
    this.setState({
      destinationCoordinates: e
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
      currentLocation: {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude
      }
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
    console.log(this.state.currentLocation);

    return (
      <div>
        <div className="EntireBox SearchByDestinationBox bg-light container col-md-12  position-absolute  ">
          <div className="container ">
            <AppViewHeader SearchState={"Search By Destination"} />
            <AppViewFavourAndLogin />
            <div id="formColor">
              <form>
                <div className="container border border-secondary SearchByDestinationForm">
                  <div className="row row_first border border-secondary">
                    <h5>Where:</h5>
                  </div>

                  <div className="row row_second border border-secondary">
                    <div className="col-5 border border-secondary">
                      <label> Start Point:</label>
                    </div>
                    <div className="col-7  border border-secondary">
                      {/*<input type="text"/>*/}
                      <GoogleAddressSearch
                        onUpdatePosition={this.updateCurrentPosition}
                        comment="Current Location"
                      />
                    </div>
                  </div>

                  <div className="row row_third border border-secondary">
                    <div className="col-4 border border-secondary">
                      <label htmlFor="fname"> Destination:</label>
                    </div>
                    <div className="col-7  border border-secondary">
                      <GoogleAddressSearch
                        onUpdatePosition={this.setDestination}
                        comment="Set Your Destination"
                      />
                    </div>
                  </div>

                  <h6>+Add Multi Routes</h6>

                  <div className="row row_fourth border border-secondary">
                    <div className="col-3   border border-secondary">
                      <p>Filter :</p>
                    </div>
                    <div className="col-3 form-check  border border-secondary">
                      <input
                        type="checkbox"
                        className="form-check-input"
                        id="BusCheckBoc"
                      />
                      <label className="form-check-label">Bus</label>
                    </div>
                    <div className="col-3 form-check  border border-secondary">
                      <input
                        type="checkbox"
                        className="form-check-input"
                        id="LuasCheckBox"
                      />
                      <label className="form-check-label">Luas</label>
                    </div>
                    <div className="col-3 form-check  border border-secondary">
                      <input
                        type="checkbox"
                        className="form-check-input"
                        id="TrainCheckBox"
                      />
                      <label className="form-check-label">Train</label>
                    </div>
                    <h5>When: </h5>
                  </div>

                  <div className="row row_fifth border border-secondary">
                    <div className="col-4 border border-secondary">
                      <label> Date:</label>
                    </div>
                    <div className="col-8 cc border border-secondary">
                      <DatePicker
                        selected={this.state.initial_Date}
                        onChange={this.handleChangeDate}
                        placeholderText="Today"
                      />
                    </div>
                  </div>

                  <div className="row row_fifth border border-secondary">
                    <div className="col-4 border border-secondary">
                      <label> Time:</label>
                    </div>
                    <div className="col-8 cc border border-secondary">
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
                </div>
              </form>
            </div>

            <div className="row NotificationButton border border-secondary">
              <p>NotificationButton locate here</p>
            </div>

            <Link
              to={`/ResultPageDestination/${this.state.startCoordinates}/${this.state.destinationCoordinates}/${this.state.startDateToBackEnd}/${this.state.startTimeToBackEnd}`}>
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
          </div>
        </div>
      </div>
    );
  }
}

export default SearchbyDestination;
