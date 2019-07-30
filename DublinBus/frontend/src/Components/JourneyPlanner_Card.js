import Imgx from "../Static/img/img1.jpg";
import React from "react";
import "../Static/StyleSheet/JourneyPlanner_Card.css";
class JourneyPlanner_Card extends React.Component {
  render() {
    return (
      <div className="card col-10 Card_allAttraction">
        <img className="card-img-top" src={Imgx} alt="Card image cap" />

        <div className="card-body">
          <h5>{props.name}</h5>
          <p className="card-text">{props.description}</p>
        </div>
        <a type="button" className=" btn btn-success col-6">
          <p>
            <i className="fas fa-plus"></i>
          </p>
        </a>
      </div>
    );
  }
}
export default JourneyPlanner_Card;
