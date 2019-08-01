import React from "react";
import GoogleAddressSearch from "./GoogleAddressSearch";
import "../Static/StyleSheet/YourLocationOrSearch.css";

import { FaCrosshairs, FaSearchLocation } from "react-icons/fa";

class YourLocationOrSearch extends React.Component {
  constructor(props) {
    super(props);
    this.state = { inputText: "From Your Current Location", mode: "view" };

    this.handleSave = this.handleSave.bind(this);
    this.handleEdit = this.handleEdit.bind(this);
  }

  handleSave() {
    this.setState({ mode: "view" });
  }

  handleEdit() {
    this.setState({ mode: "edit" });
  }

  renderInputField() {
    if (this.state.mode === "view") {
      return (
        <div>
          <GoogleAddressSearch
            comment="Set Your Start Point"
          onUpdatePosition={this.props.onUpdatePosition}
          onUpdateHome={this.props.onUpdateHome}
          />
        </div>
      );
    } else {
      return (
        <input
          id="InputBoxYourLocationOrSearch"
          value={this.state.inputText}
          disabled
        />
      );
    }
  }

  renderButton() {
    let button;

    if (this.state.mode === "view") {
      button = (
        <div>
          <a onClick={this.handleEdit}>
            <FaCrosshairs className="icon" />
          </a>
        </div>
      );
    } else {
      button = (
        <a onClick={this.handleSave}>
          <FaSearchLocation className="icon" />
        </a>
      );
    }

    return button;
  }

  render() {
    return (
      <div YourLocationOrSearch className="row">
        <div className="col-10 ">{this.renderInputField()}</div>
        <div className="col-2  ClickChangeInput">{this.renderButton()}</div>
      </div>
    );
  }
}

export default YourLocationOrSearch;
