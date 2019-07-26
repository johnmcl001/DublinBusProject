<<<<<<< HEAD
import React from "react";
import Imgx from "../Static/img/img1.jpg";

class JouneryPlanner_ToVisitPiont extends React.Component {
  render() {
    return (
      <React.Fragment>
        <a
          className="btn  btn-success border border-secondary "
          id={this.props.buttonID}
          data-toggle="modal"
          href={`#${this.props.cardID}`}
          aria-expanded="false"
        >
          <p>
            <i className="fab fa-fort-awesome-alt "></i>
          </p>
        </a>

        <div
          className="modal fade "
          id={this.props.cardID}
          tabindex="-1"
          role="dialog"
          aria-labelledby="exampleModalCenterTitle"
          aria-hidden="true"
        >
          <div className="modal-dialog  modal-dialog-centered" role="document">
            <div className="modal-content">
              <div className="modal-header border border-success">
                <h4 className="modal-title" id="exampleModalLongTitle">
                  Attraction Name
                </h4>
                <button
                  type="button"
                  className="close  border border-success"
                  data-dismiss="modal"
                  aria-label="Close"
                >
                  X
                </button>
              </div>

              <div className="card">
                <img className="card-img-top" src={Imgx} alt="Card image cap" />

                <div className="card-body">
                  <p className="card-text">
                    Some quick example text to build on the card title and make
                    up the bulk of the card's contentSome quick example text to
                    build on the card title and make up the bulk of the card's
                    contentSome quick example text to build on the card title
                    and make up the bulk of the card's content.
                  </p>
                </div>
              </div>
              <button
                type="button"
                className="Delete_bottom btn btn-info col-6"
              >
                Remove it from list?
              </button>
            </div>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default JouneryPlanner_ToVisitPiont;
=======
import React from 'react'
import Imgx from "../Static/img/img1.jpg";

class JouneryPlanner_ToVisitPiont extends React.Component {
    render() {
        return (
            <React.Fragment>
                <a className='btn  btn-success border border-secondary ' id={this.props.buttonID}
                   data-toggle="modal" href={`#${this.props.cardID}`} aria-expanded="false"><p><i
                    className="fab fa-fort-awesome-alt "></i></p></a>


                <div className="modal fade " id={this.props.cardID} tabindex="-1" role="dialog"
                     aria-labelledby="exampleModalCenterTitle" aria-hidden="true">

                    <div className="modal-dialog  modal-dialog-centered" role="document">

                        <div className="modal-content">

                            <div className="modal-header border border-success">
                                <h4 className="modal-title" id="exampleModalLongTitle">Attraction Name</h4>
                                <button type="button" className="close  border border-success" data-dismiss="modal"
                                        aria-label="Close">
                                    X
                                </button>
                            </div>

                            <div className="card">
                                <img className="card-img-top" src={Imgx} alt="Card image cap"/>

                                <div className="card-body">
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

                            </div>
                            <button type="button" className="Delete_bottom btn btn-info col-6">Remove it from list?
                            </button>
                        </div>
                    </div>
                </div>
            </React.Fragment>);
    }
}

export default JouneryPlanner_ToVisitPiont;
>>>>>>> JourneyPlanner
