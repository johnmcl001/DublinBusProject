import React, { Component } from "react";
import { Link } from "react-router-dom";
import "../Static/StyleSheet/SearchbyDestination.css";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import YourLocationOrSearch from "./YourLocationOrSearch";
import GoogleAddressSearch from "./GoogleAddressSearch";
import { FaMapMarkerAlt } from "react-icons/fa";

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

      //Location Co-Ordinate start Here
      currentLocation_lat: null,
      currentLocation_long: null,

      startLocation_lat: null,
      startLocation_long: null,

      destination_lat: null,
      destination_long: null,

      start: "",
      end: ""
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
      startLocation_lat: e.latitude,
      startLocation_long: e.longitude,
      start: e.place
    });
  }

  setDestination(e) {
    //set Co-ordinate for destination box
    this.setState({
      destination_lat: e.latitude,
      destination_long: e.longitude,
      end: e.place
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
      startTimeToBackEnd: Time.getHours() + ":" + Time.getMinutes() + ":" + Time.getSeconds()
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
        <div className="EntireBox  SearchByDestinationBox bg-light container col-md-12  position-absolute  ">
          {/*<div className='container '>*/}
          <AppViewHeader
            SearchState={"Search By Destination"}
            Return="toHomePage"
          />
          <AppViewFavourAndLogin />
          <div id="formColor">
            <form>
              <div className="container  SearchByDestinationForm">
                <div className="row row_first ">
                  <h5 id="whereLabel">Where:</h5>
                </div>

                <div className="row row_second">
                  <div className="col-12 DestinationAddressLabel ">
                    <label> Start Point:</label>
                  </div>

                  <div className="col-10 row_input ">
                    <YourLocationOrSearch
                      onUpdatePosition={this.updateCurrentPosition}
                    />
                  </div>
                </div>

                <div className="row row_third  ">
                  <div className="col-12 DestinationAddressLabel ">
                    <label> Destination:</label>
                  </div>
                </div>
                <div className="row">
                  <div className="col-8 row_input  " id="destination_Input">
                    <GoogleAddressSearch
                      onUpdatePosition={this.setDestination}
                      comment="Set Your Destination"
                    />
                  </div>
                  <div className="col-2 ">
                    <FaMapMarkerAlt className="icon " id="icon_destination" />
                  </div>
                </div>

                <h6>+Add Multi Routes</h6>

                <div className="row row_fourth ">
                  <div className="col-3  row_input row_input  ">
                    <p>Filter :</p>
                  </div>
                  <div className="col-3  row_input form-check  ">
                    <input
                      type="checkbox"
                      row_input
                      className="form-check-input"
                      id="BusCheckBoc"
                    />
                    <label className="form-check-label">Bus</label>
                  </div>
                  <div className="col-3 row_input form-check ">
                    <input
                      type="checkbox"
                      className="form-check-input"
                      id="LuasCheckBox"
                    />
                    <label className="form-check-label">Luas</label>
                  </div>
                  <div className="col-3 row_input form-check ">
                    <input
                      type="checkbox"
                      className="form-check-input"
                      id="TrainCheckBox"
                    />
                    <label className="form-check-label">Train</label>
                  </div>
                </div>

                <h5>When: </h5>

                <div className="row row_fifth ">
                  <div className="col-4 ">
                    <label> Date:</label>
                  </div>
                  <div className="col-8  ">
                    <DatePicker
                      selected={this.state.initial_Date}
                      onChange={this.handleChangeDate}
                      placeholderText="Today"
                    />
                  </div>
                </div>

                <div className="row row_fifth ">
                  <div className="col-4  ">
                    <label> Time:</label>
                  </div>
                  <div className="col-8 ">
                    <DatePicker
                      selected={this.state.initial_Time}
                      onChange={this.handleChangeTime}
                      showTimeSelect
                      showTimeSelectOnly
                      timeIntervals={15}
                      dateFormat="hh:mm:ss aa"
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
            to={`/ResultPageDestination/${this.state.startLocation_lat}/${this.state.startLocation_long}/${this.state.destination_lat}/${this.state.destination_long}/${this.state.startDateToBackEnd}/${this.state.startTimeToBackEnd}/${this.state.start}/${this.state.end}`}
          >
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
      </div>
    );
  }
}

export default SearchbyDestination;
