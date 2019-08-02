import React, {Component} from "react";
import {Link} from "react-router-dom";
import "../Static/StyleSheet/SearchbyDestination.css";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import YourLocationOrSearch from "./YourLocationOrSearch";
import GoogleAddressSearch from "./GoogleAddressSearch";
import {FaMapMarkerAlt} from "react-icons/fa";
import WarningAlert from "./WarningAlert";
import * as $ from "jquery";
// npm install react-datepicker --save
import DatePicker from "react-datepicker";
import { addDays } from 'date-fns';


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

            startLat: '',
            startLon: null,

            destinationLat: '',
            destinationLon: null,

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

    checkEmpty() {
        {
            //    To activate Warning alert
        }
        if (this.state.startLat.length == 0) {

            this.setState({
                warningText: 'Hey, Please Pick Your Start Point'
            });
            let $ = jQuery;

            (function ($) {
                $('#DestinationWarning').modal('toggle')
            })(jQuery);

        } else if (this.state.destinationLat.length == 0) {

            this.setState({
                warningText: 'Hey, Please Pick Your Destination Point'
            });

            (function ($) {
                $('#DestinationWarning').modal('toggle')
            })(jQuery);
        } else {
            this.props.history.push(`/ResultPageDestination/${this.state.startLat}/${this.state.startLon}/${this.state.destinationLat}/${this.state.destinationLon}/${this.state.startDateToBackEnd}/${this.state.startTimeToBackEnd}/${this.state.start}/${this.state.end}`);
        }
    }


    updateCurrentPosition(e) {
        this.setState({
            startLat: e.latitude,
            startLon: e.longitude,
            start: e.home
        });
    }

    setDestination(e) {
        //set Co-ordinate for destination box
        this.setState({
            destinationLat: e.latitude,
            destinationLon: e.longitude,
            end: e.home
        });
    }

    handleChangeDate(date) {
        //set date
        var day = date.getDate() < 10 ? "0" + date.getDate() : date.getDate()
        var month = date.getMonth() < 10 ? "0" + (date.getMonth() + 1) : date.getMonth() + 1
        this.setState({
            initial_Date: date,
            startDateToBackEnd:
                day + "-" + month + "-" + date.getFullYear()
        });
    }

    handleChangeTime(Time) {
        //set time
        this.setState({
            initial_Time: Time,
            startTimeToBackEnd:
                Time.getHours() + ":" + Time.getMinutes()
        });
    }

    //This is Geolocation ask for current location
    setPosition(position) {
        this.setState({
            currentLocation_lat: position.coords.latitude,
            currentLocation_lon: position.coords.longitude
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
        console.log(this.props)
    }


    render() {


        return (
            <div>
                <div className="EntireBox  SearchByDestinationBox bg-light container col-md-12  position-absolute  ">
                    {/*<div className='container '>*/}
                    <AppViewHeader
                        SearchState={"Search By Destination"}
                        Return="toHomePage"
                    />
                    <AppViewFavourAndLogin/>
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
                                            id='AddressAutoStart'
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
                                            id='AddressAutoDestination'
                                        />

                                    </div>
                                    <div className="col-2 ">
                                        <FaMapMarkerAlt className="icon " id="icon_destination"/>
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
                                            minDate={new Date()}
                                            maxDate={addDays(new Date(), 9)}
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



                    <button
                        type="button"
                        className="btn btn-warning col-7"
                        id="SubmitButton"
                        onClick={this.checkEmpty.bind(this)}

                    >
                        Submit
                    </button>


                </div>
                <WarningAlert color={'#F65314'} id={'DestinationWarning'} title={'Warning'}
                              content={this.state.warningText}

                />

            </div>
        );
    }
}

export default SearchbyDestination;
