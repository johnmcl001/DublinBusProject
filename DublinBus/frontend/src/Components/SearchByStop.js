import React, { Component } from "react";
//mport {FaBeer} from 'react-icons/fa';
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import "../Static/StyleSheet/StyleSearchByStop.css";

import AppViewHeader from "./AppViewHeader";

class SearchByStop extends Component {
  render() {
    return (
      <div className="EntireBox SearchByStop container position-absolute col-md-12 bg-light">
        {/*<div className=' bg-light  ' >*/}
        <AppViewHeader />
        <AppViewFavourAndLogin />
        <div className="col-12" id="formColor">
          <form id="SearchByStopForm">
            <label htmlFor="fname">Stop Number : </label>

            <input type="text" />
          </form>
        </div>

        <button
          type="button"
          className="btn btn-warning col-7"
          id="SubmitButton"
        >
          Submit
        </button>

        {/*</div>*/}
      </div>
    );
  }
}

export default SearchByStop;
