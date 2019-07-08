import React, {Component} from 'react';
import '../Static/StyleSheet/SearchByRoute.css'
import AppViewHeader from "./AppViewHeader"
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import {Link} from "react-router-dom";

//This Component is Search by Route at the mobile view ports
class SearchByRoute extends Component {
    state = {SearchState: 'Search By Route'}

    render() {
        return (
            <div className='EntireBox SearchByRoute container col-md-12  position-absolute' id='EntireBox_SearchRoute'>
                <div className='container SearchByRouteBox bg-light'>
                    <AppViewHeader SearchState={this.state.SearchState}/>
                    <AppViewFavourAndLogin/>
                    <div id='formColor'>
                        <form>
                            <div className='row row_first'>
                            </div>
                            <div className='row rowSpace '>

                                <div className='col-5 RouteNumber  '>
                                    <label htmlFor="fname"> Route Number :</label>
                                </div>
                                <div className='col-7 RouteNumber inputBox'>
                                    <input type="text"/>
                                </div>
                            </div>


                            <div className="row rowSpace">
                                <div className="col-5  ">
                                    <label htmlFor="Towards">Towards :</label>
                                </div>
                                <div className="col-7 inputBox">
                                    <select id="towards" name="towards">
                                        <option value="australia"> </option>
                                        <option value="canada"> ss</option>

                                    </select>
                                </div>
                            </div>


                            <div className='row rowSpace '>
                                <div className='col-5 '>
                                    <label htmlFor="fname"> Departure :</label>
                                </div>
                                <div className='col-7  inputBox'>
                                    <input type="text"/>
                                </div>


                            </div>
                        </form>

                    </div>

                <Link to={'/ResultPage_Stop_Route'}><button type="button" className="btn btn-warning col-7"
                        id='SubmitButton'>Submit</button></Link>
                </div>
            </div>
        );
    }

}


export default SearchByRoute;
