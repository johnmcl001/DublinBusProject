import React, {Component} from "react";
import "../Static/StyleSheet/JourneyPlanner_Table.css"
import "../Static/StyleSheet/ResultPageDestination.css";
import {Button, Accordion} from 'react-bootstrap';
import {FaWalking, FaLevelDownAlt, FaMapMarkerAlt} from "react-icons/fa";


//This Component is the table which displays the results at Journey Planner Result page.
class JourneyPlanner_Table extends React.Component {

    render() {
        const color = this.props.color;
        return (

            <React.Fragment>

                {/*This is the show section ,which displays the name of the attraction*/}
                <div className=" resultDisplay">
                    <Accordion.Toggle className=' JourneyPlanner_Table '
                                      style={{borderTop: `5px solid ${color}`}}
                                      as={Button} variant="link"
                                      eventKey={this.props.buttonID}>
                        <div className='row'>

                            <div className=' NumberContainer '>
                                <div className=' position-relative ShowOrders  '
                                     style={{backgroundColor: color}}>
                                    <p className='NumberingOrders  position-absolute '>{this.props.number}</p>

                                </div>
                            </div>
                                    <h5 className=' AttractionName'
                                        style={{color: this.props.color}}>Guinness
                                        Storehouse container containercontainer</h5>
                                </div>
                    </Accordion.Toggle>
                </div>



                    {/*This is the collapsed section  ,
                            it will open and show user the instruction if user click attraction display shown above */}
                <div className="row ">

                    <Accordion.Collapse className=" JourneyPlannerResultDisplay" eventKey={this.props.buttonID}
                    >
                        <div className="card TableCardBody card-body col-11" style={{
                            borderColor: color, borderWidth: '2px '
                        }}>

                            {/*If Map loops Start From here*/}
                            <div>
                                <div className="row instruction " style={{backgroundColor: color}}>
                                    <p className="Icons_ResultPage ">
                                        <FaWalking className="Icon"/>
                                    </p>
                                    <p className="instruction_text ">
                                        Walk to O'Conned Street
                                    </p>
                                    <p className="time_show ">6 mins</p>
                                </div>
                                <FaLevelDownAlt className="arrow_down_icon "/>
                            </div>
                            {/*Ends Here*/}




                            <div className="row result_destination  " style={{backgroundColor: color}}>
                                <p className="Icons_destination ">
                                    <FaMapMarkerAlt className="Icon"/>
                                </p>

                                <p className="destination_text ">
                                    Your Destination
                                </p>
                            </div>
                        </div>

                    </Accordion.Collapse>


                </div>
            </React.Fragment>);
    }
}

export default JourneyPlanner_Table