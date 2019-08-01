import React from 'react'
import {FaInfoCircle} from "react-icons/fa";
//import "../Static/StyleSheet/WarningAlert.css";

//This is Component is the attraction that tourist selected and planed to visit



class WarningAlert extends React.Component {


    render() {

        return (


            <React.Fragment>
                <div className="modal fade col-sm-12 warningModel" id="JourneyPlannerAlertBox" tabIndex="-1" role="alert"
                     aria-labelledby="exampleModalLabel" aria-hidden="false">
                    <div className="modal-dialog" role="document">
                        <div className="modal-content">
                            {/*Warning heading start here*/}
                            <div className="modal-header CapWarning " style={{backgroundColor:this.props.color}}>
                                <h4 >Information</h4>
                                <button type="button" className="close " data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                                                        {/*Warning heading Ends here*/}


                            <div className="modal-body row">
                                <div className="col-4 ">
                                    <FaInfoCircle className='WarningIcon' size={70} style={{color: this.props.color}}/>
                                </div>
                                <div className="col-8 CapWarningContext">
                                    Sorry, You can only select five attraction.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </React.Fragment>);
    }
}

export default WarningAlert;
