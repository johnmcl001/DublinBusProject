import React, { Component } from "react";
import "../Static/StyleSheet/SearchByRoute.css";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";

class SearchByRoute extends Component {
  render() {
    return (
      <div className=" EntireBox SearchByRoute container col-md-12  position-absolute">
        <div className="container SearchByRouteBox bg-light">
          <AppViewHeader />
          <AppViewFavourAndLogin />
          <div id="formColor">
            <form>
              <div className="row row_first"></div>
              <div className="row rowSpace border border-primary">
                <div className="col-5 RouteNumber  border border-primary">
                  <label htmlFor="fname"> Route Number :</label>
                </div>
                <div className="col-7 RouteNumber inputBox">
                  <input type="text" />
                </div>
              </div>

              <div className="row rowSpace border border-primary">
                <div className="col-5  ">
                  <label htmlFor="Towards">Towards :</label>
                </div>
                <div className="col-7 inputBox">
                  <select id="towards" name="towards">
                    <option value="australia">to be input</option>
                    <option value="canada">to be input</option>
                  </select>
                </div>
              </div>

              <div className="row rowSpace border border-primary">
                <div className="col-5 ">
                  <label htmlFor="fname"> Departure :</label>
                </div>
                <div className="col-7  inputBox">
                  <input type="text" />
                </div>
              </div>
            </form>
          </div>

          <button
            type="button"
            className="btn btn-warning col-7"
            id="SubmitButton"
          >
            Submit
          </button>
        </div>
      </div>
    );
  }
}

export default SearchByRoute;
