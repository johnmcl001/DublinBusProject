import React, { Component } from "react";

//This Component is Errero handling Component ,
// It will render out if there is no match URL.

class NoPathToRender_ThenThisPage extends Component {
  render() {
    return (
      <div className="position-absolute" style={error404Sytle}>
        <h1>Error 404 !</h1>
        <h2>Your Page Cant Be Find</h2>
      </div>
    );
  }
}

const error404Sytle = {
  marginLeft: "auto",
  marginRight: "auto",
  marginTop: "auto",
  marginBottom: "auto",
  left: "0",
  right: "0",
  top: "0",
  bottom: "100px",

  backgroundColor: "lightgrey",
  width: "50%",
  height: "30%"
};

export default NoPathToRender_ThenThisPage;
