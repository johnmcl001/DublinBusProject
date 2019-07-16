import React, { Component } from "react";
import "../Static/StyleSheet/DropDownNav.css";

class DropDownNav extends Component {
  render() {
    return (
      <div className="dropdown dropdown">
        <button
          className="btn btn-light  "
          type="button"
          id="dropdownMenu2"
          data-toggle="dropdown"
          aria-haspopup="true"
          aria-expanded="false"
        >
          ☰
        </button>

        <div
          className="dropdown-menu dropdown-menu-right"
          aria-labelledby="dropdownMenu2"
        >
          <button className="dropdown-item  " type="button">
            Home
          </button>
          <button className="dropdown-item" type="button">
            About
          </button>
          <button className="dropdown-item" type="button">
            Service
          </button>
        </div>
      </div>
    );
  }
}

export default DropDownNav;
