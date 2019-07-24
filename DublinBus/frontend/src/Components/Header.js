import React, { Component } from "react";
import logo from "./Route13-log.png";
import Login from "./Login";
import FavourPage from "./FavourPage";
import { Link } from "react-router-dom";
import "../Static/StyleSheet/Header.css";

class Header extends Component {
  render() {
    return (
      <nav className="navbar navbar-expand-md navbar-light bg-light sticky-top d-none d-lg-block d-md-none Header">
        {/*Stick to top , and Hidden navigation bar if screen medium screen size */}
        <div className="container-fluid">
          <a className="navbar-brand" id="BrandName">
            <img style={navLogoStyle} src={logo} /> Route 13{" "}
          </a>

          <div className="mr-auto  ">
            {/*Margin right*/}
            <ul className="navbar-nav ">
              <li className="nav-item active ">
                <a
                  className="nav-link"
                  onClick={() => window.location.replace("./")}
                >
                  Home
                </a>
              </li>
              <li className="nav-item ">
                <a className="nav-link" href="#">
                  About
                </a>
              </li>
              <li className="nav-item ">
                <a className="nav-link" href="#">
                  Service
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#">
                  Team
                </a>
              </li>
            </ul>
          </div>
          {/*<Login/>*/}
          {/*<FavourPage/>*/}
          <form className="form-inline">
            <input
              className="form-control mr-sm-2"
              type="search"
              placeholder="Search"
              aria-label="Search"
            />
            <button
              className="btn btn-outline-success my-2 my-sm-0"
              type="submit"
            >
              Search
            </button>
          </form>
        </div>
      </nav>
    );
  }
}
const navLogoStyle = {
  width: "2.5em",
  height: "2.5em"
};

export default Header;
