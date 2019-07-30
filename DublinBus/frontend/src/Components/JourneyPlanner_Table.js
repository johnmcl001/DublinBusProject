import React, { Component } from "react";
import "../Static/StyleSheet/JourneyPlanner_Table.css";

class JourneyPlanner_Table extends React.Component {
  render() {
    const color = this.props.color;
    return (
      <React.Fragment>
        <div
          className="row position-relative JourneyPlanner_Table col-11  "
          style={{ borderTop: `5px solid ${color}` }}
          id={this.props.buttonID}
          data-toggle="collapse"
          href={`#${this.props.cardID}`}
          aria-expanded="false"
        >
          <div
            className="col-2  ShowOrders position-absolute"
            style={{ backgroundColor: color }}
          >
            <p className="NumberingOrders position-absolute">
              {this.props.number}
            </p>
          </div>
          <h4
            className="col-10 AttractionName "
            style={{ color: this.props.color }}
          >
            {this.props.attraction}
          </h4>
        </div>
        <div className="row ">
          <div
            className="collapse "
            id={this.props.cardID}
            data-parent="#accordionExample"
          >
            <div
              className="card TableCardBody card-body col-11"
              style={{ borderColor: color, borderWidth: "2px " }}
            >
              {this.props.description}
            </div>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default JourneyPlanner_Table;
