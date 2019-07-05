import React, { Component } from "react";
import logo from "./Route13-log.png";
import Login from "./Login";
import FavourPage from "./FavourPage";

class Header extends Component {
  render() {
    return (
      <nav className="navbar navbar-expand-md navbar-light bg-light sticky-top d-none d-lg-block d-md-none">
        {/*Stick to top , and Hidden navigation bar if screen medium screen size */}
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            <img style={navLogoStyle} src={logo} />{" "}
          </a>

          <div className="mr-auto">
            {/*Margin right*/}
            <ul className="navbar-nav ">
              <li className="nav-item active ">
                <a className="nav-link" href="#">
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
          <Login />
          <FavourPage />
        </div>
      </nav>
    );
  }
}
const navLogoStyle = {
  width: "3em",
  height: "3em"
};

export default Header;
