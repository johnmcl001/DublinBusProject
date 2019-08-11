import React from "react";
import {
    FaWalking,
    FaLevelDownAlt,
    FaMapMarkerAlt,
    FaBus
} from "react-icons/fa";


{
//    This Component is used in Result Page Destination , For the purpose of displaying route instruction
}
const Table = ({data}) =>
    !data.length ? (
        <p>Nothing to show</p>
    ) : (
        <div>
            <div className="row "></div>

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
                                {data[0].duration} Mins
                            </a>
                        </li>
                        {/*
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
                {data[1].duration} Mins
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
                {data[2].duration} Mins
              </a>
            </li>
           */}
                    </ul>

                    <div className="tab-content" id="pills-tabContent">
                        <div
                            className="tab-pane fade show active"
                            id="pills-home"
                            role="tabpanel"
                            aria-labelledby="pills-home-tab"
                        >
                            {data[0].directions.map((x, y) => (
                                //    Loop throught
                                <div key={y}>
                                    <div className="row instruction  ">
                                        <p className="Icons_ResultPage ">
                                            {x.travel_mode == "WALKING" ? (
                                                <FaWalking className="Icon"/>
                                            ) : (
                                                <FaBus className="Icon"/>
                                            )}
                                        </p>
                                        <p
                                            className="instruction_text"

                                        >
                                            {x.instruction}
                                        </p>
                                        <p className="time_show ">
                                            {x.time} mins
                                        </p>
                                    </div>
                                    <FaLevelDownAlt className="arrow_down_icon "/>

                                </div>
                            ))}

                            <div className="row result_destination  ">
                                <p className="Icons_destination ">
                                    <FaMapMarkerAlt className="Icon"/>
                                </p>

                                <p className="destination_text ">
                                    Your Destination
                                </p>
                            </div>
                        </div>
                        {/*
            <div
              className="tab-pane fade"
              id="pills-profile"
              role="tabpanel"
              aria-labelledby="pills-profile-tab"
            >
              {data[1].directions.map((x, y) => (
                //    Loop throught
                <div>
                  <div className="row instruction  ">
                    <p className="Icons_ResultPage ">
                      {x.travel_mode == "WALKING" ? (
                        <FaWalking className="Icon" />
                      ) : (
                        <FaBus className="Icon" />
                      )}
                    </p>
                    <p
                      className="instruction_text "
                      key={y}
                    >
                      {x.instruction}
                    </p>
                    <p className="time_show " key={y}>
                      {x.time} mins
                    </p>
                  </div>
                                                                    <FaLevelDownAlt className="arrow_down_icon "/>

                </div>
              ))}
                            <div className="row result_destination  " >
                                <p className="Icons_destination ">
                                    <FaMapMarkerAlt className="Icon"/>
                                </p>

                                <p className="destination_text ">
                                    Your Destination
                                </p>
                            </div>
            </div>
            <div
              className="tab-pane fade"
              id="pills-contact"
              role="tabpanel"
              aria-labelledby="pills-contact-tab"
            >
              {data[2].directions.map((x, y) => (
                //    Loop throught
                <div>
                  <div className="row instruction border border-secondary ">
                    <p className="Icons_ResultPage border border-secondary">
                      {x.travel_mode == "WALKING" ? (
                        <FaWalking className="Icon" />
                      ) : (
                        <FaBus className="Icon" />
                      )}
                    </p>
                    <p
                      className="instruction_text border border-secondary"
                      key={y}
                    >
                      {x.instruction}
                    </p>
                    <p className="time_show border border-secondary" key={y}>
                      {x.time} mins
                    </p>
                  </div>
                </div>
              ))}
                            <div className="row result_destination  " >
                                <p className="Icons_destination ">
                                    <FaMapMarkerAlt className="Icon"/>
                                </p>

                                <p className="destination_text ">
                                    Your Destination
                                </p>
                            </div>
                                                                                                <FaLevelDownAlt className="arrow_down_icon "/>

            </div>
                      */}
                    </div>
                </div>
            </div>
            <div></div>
        </div>
    );

export default Table;
