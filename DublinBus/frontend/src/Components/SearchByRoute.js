import React, { Component } from "react";
import "../Static/StyleSheet/SearchByRoute.css";
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import { Link } from "react-router-dom";

/*
  SQL Query Template
  select distinct s.stopID_short, s.stop_name
  from stops s, stop_times st, trips t, routes r, calendar c
  where s.stop_id = st.stop_id and
  st.trip_id = t.trip_id and
  t.route_id = r.route_id and
  t.service_id = c.service_id and
  r.route_short_name = <route> and
  st.stop_headsign = <direction> and
  c.<day> = 1;
  Example route: 46a
  Example direction: Phoenix Pk
  Example day: monday
*/

//This Component is Search by Route at the mobile view ports
class SearchByRoute extends Component {
  state = { SearchState: "Search By Route" };

  render() {
    return (
      <div
        className="EntireBox SearchByRoute container col-md-12  position-absolute"
        id="EntireBox_SearchRoute"
      >
        <div className="container SearchByRouteBox bg-light">
          <AppViewHeader SearchState={this.state.SearchState} />
          <AppViewFavourAndLogin />
          <div id="formColor">
            <form>
              <div className="row row_first"></div>
              <div className="row rowSpace ">
                <div className="col-5 RouteNumber  ">
                  <label htmlFor="fname"> Route Number :</label>
                </div>
                <div className="col-7 RouteNumber inputBox">
                  <input type="text" />
                </div>
              </div>

              <div className="row rowSpace">
                <div className="col-5  ">
                  <label htmlFor="Towards">Towards :</label>
                </div>
                <div className="col-7 inputBox">
                  <select id="towards" name="towards">
                    <option value="australia"> </option>
                    <option value="canada"> ss</option>
                  </select>
                </div>
              </div>

              <div className="row rowSpace ">
                <div className="col-5 ">
                  <label htmlFor="fname"> Departure :</label>
                </div>
                <div className="col-7  inputBox">
                  <input type="text" />
                </div>
              </div>
            </form>
          </div>

          <Link to={"/ResultPage_Stop_Route"}>
            <button
              type="button"
              className="btn btn-warning col-7"
              id="SubmitButton"
            >
              Submit
            </button>
          </Link>
        </div>
      </div>
    );
  }
}

export default SearchByRoute;
