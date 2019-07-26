import Imgx from "../Static/img/img1.jpg";
import React from "react";
import "../Static/StyleSheet/JourneyPlanner_Card.css";
class JourneyPlanner_Card extends React.Component {
  render() {
    return(<div className="card col-10 Card_allAttraction">

        <img className="card-img-top" src={Imgx} alt="Card image cap"/>

        <div className="card-body">
            <h5>Title</h5>
            <p className="card-text">Some quick example text to build on the card title and make
                up the
                bulk of the card's contentSome quick example text to build on the card title and
                make
                up the
                bulk of the card's contentSome quick example text to build on the card title and
                make
                up the
                bulk of the card's content.</p>
        </div>
        <a type="button" className=" btn btn-success col-6"><p><i className="fas fa-plus"></i>
        </p>
        </a>
    </div>);
  }
}
export default JourneyPlanner_Card