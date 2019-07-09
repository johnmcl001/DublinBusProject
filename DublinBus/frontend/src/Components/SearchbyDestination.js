import React, { Component } from "react";
import { Link } from "react-router-dom";
import "../Static/StyleSheet/SearchbyDestination.css";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";

// import DatePicker from 'react-datepicker';
//This Component is Search by Destination at the mobile view ports
class SearchbyDestination extends Component {
  render() {
    return (
      <div>
        <div className="EntireBox SearchByDestinationBox bg-light container col-md-12  position-absolute">
          <div className="container ">
            <AppViewHeader SearchState={"Search By Destination"} />
            <AppViewFavourAndLogin />
            <div id="formColor">
              <form>
                <div className="container SearchByDestinationForm">
                  <div className="row row_first border border-secondary">
                    <h4>Where</h4>
                  </div>

                  <div className="row row_second border border-secondary">
                    <div className="col-5 border border-secondary">
                      <label htmlFor="fname"> Start Point:</label>
                    </div>
                    <div className="col-7  border border-secondary">
                      <input type="text" />
                    </div>
                  </div>

                  <div className="row row_third border border-secondary">
                    <div className="col-5 border border-secondary">
                      <label htmlFor="fname"> Destination:</label>
                    </div>
                    <div className="col-7  border border-secondary">
                      <input type="text" />
                    </div>
                  </div>

                  <p>+Add Multi Routes</p>

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
                      <label
                        className="form-check-label"
                        htmlFor="exampleCheck1"
                      >
                        Train
                      </label>
                    </div>
                    <p>When</p>
                  </div>
                  <div className="row row_fifth border border-secondary">
                    <div className="col-5 border border-secondary">
                      <label htmlFor="fname"> Destination:</label>
                    </div>
                    <div className="col-7  border border-secondary">
                      <input type="text" />
                    </div>
                  </div>

                  <div className="row row_fifth border border-secondary">
                    <div className="col-5 border border-secondary">
                      <label htmlFor="fname"> Date:</label>
                    </div>
                    <div className="col-7  border border-secondary">
                      {/*<DatePicker*/}
                      {/*    selected={this.state.startDate}*/}
                      {/*    onChange={this.handleChange}*/}
                      {/*    isClearable={true}*/}
                      {/*    placeholderText="I have been cleared!"*/}
                      {/*/>*/}
                    </div>
                  </div>
                  <div className="row NotificationButton border border-secondary">
                    <p>NotificationButton locate here</p>
                  </div>
                  <Link to={"./ResultPageDestination"}>
                    {" "}
                    <button
                      type="button"
                      className="btn btn-warning col-7"
                      id="SubmitButton"
                    >
                      Submit
                    </button>
                  </Link>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default SearchbyDestination;
