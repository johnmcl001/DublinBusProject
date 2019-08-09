import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
import {
    FaWalking,
    FaLevelDownAlt,
    FaMapMarkerAlt,
    FaBus
} from "react-icons/fa";

const JourneyPlannerRouteTable = ({data}) =>
    !data.length ? (
        <p>Nothing to show</p>
    ) : (
        <div>
            <div className="container JourneyPlannerResultDisplay  "

            >

                <div className="tab-content" id="pills-tabContent">
                    <div
                        className="tab-pane fade show active"
                        id="pills-home"
                        role="tabpanel"
                        aria-labelledby="pills-home-tab">
                        {data[0].directions.map((x, y) => (
                            //    Loop throught
                            <div>
                                <div className="row instruction ">
                                    <p className="Icons_ResultPage ">
                                        {x.travel_mode == "WALKING" ? (
                                            <FaWalking className="Icon"/>
                                        ) : (
                                            <FaBus className="Icon"/>
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


                </div>

            </div>

        </div>
    );

export default JourneyPlannerRouteTable;