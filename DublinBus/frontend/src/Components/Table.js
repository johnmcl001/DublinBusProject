import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
import { FaWalking, FaLevelDownAlt, FaMapMarkerAlt } from "react-icons/fa";

const Table = ({ data }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div>
      {console.log(data)}
      <div className="row ">
        <div className="col-8 resultLabel  ">
          <h4>To 'To be Change'</h4>
        </div>
      </div>
      <div className="container border border-primary">
        <div className="container ResultPageDestination  ">
          <ul className="nav nav-pills mb-3" id="pills-tab" role="tablist">
            <li className="nav-item">
              <a
                className="nav-link active"
                id="pills-home-tab"
                data-toggle="pill"
                href="#pills-home"
                role="tab"
                aria-controls="pills-home"
                aria-selected="true"
              >
                45 Mins
              </a>
            </li>
            <li className="nav-item">
              <a
                className="nav-link"
                id="pills-profile-tab"
                data-toggle="pill"
                href="#pills-profile"
                role="tab"
                aria-controls="pills-profile"
                aria-selected="false"
              >
                67 Mins
              </a>
            </li>
            <li className="nav-item">
              <a
                className="nav-link"
                id="pills-contact-tab"
                data-toggle="pill"
                href="#pills-contact"
                role="tab"
                aria-controls="pills-contact"
                aria-selected="false"
              >
                70 Mins
              </a>
            </li>
          </ul>

          <div className="tab-content" id="pills-tabContent">
            <div
              className="tab-pane fade show active"
              id="pills-home"
              role="tabpanel"
              aria-labelledby="pills-home-tab"
            >
              {/*{props.data.map((x, y) => (*/}
              {/*//    Loop throught*/}
              {/*<div>*/}
              {/*<div className='row instruction border border-secondary '>*/}

              {/*<p className='Icons_ResultPage border border-secondary'><FaWalking*/}
              {/*className='Icon'/></p>*/}
              {/*<p className='instruction_text border border-secondary'>Walk to O'Conned*/}
              {/*Street</p>*/}
              {/*<p className='time_show border border-secondary'>6 mins</p>*/}

              {/*</div>*/}

              {/*<FaLevelDownAlt className='arrow_down_icon border border-secondary'/>*/}
              {/*</div>*/}
              {/*))}*/}

              <div>
                <div className="row instruction border border-secondary ">
                  <p className="Icons_ResultPage border border-secondary">
                    <FaWalking className="Icon" />
                  </p>
                  <p className="instruction_text border border-secondary">
                    Walk to O'Conned Street
                  </p>
                  <p className="time_show border border-secondary">6 mins</p>
                </div>
                <FaLevelDownAlt className="arrow_down_icon border border-secondary" />
              </div>

              <div className="row result_destination border border-secondary ">
                <p className="Icons_destination border border-secondary">
                  <FaMapMarkerAlt className="Icon" />
                </p>

                <p className="destination_text border border-secondary">
                  O'Conned Street
                </p>
              </div>
            </div>
            <div
              className="tab-pane fade"
              id="pills-profile"
              role="tabpanel"
              aria-labelledby="pills-profile-tab"
            >
              ...
            </div>

            <div
              className="tab-pane fade"
              id="pills-contact"
              role="tabpanel"
              aria-labelledby="pills-contact-tab"
            >
              ...
            </div>
          </div>
        </div>
      </div>
    </div>
  );

Table.propTypes = {
  data: PropTypes.array.isRequired
};

export default Table;
