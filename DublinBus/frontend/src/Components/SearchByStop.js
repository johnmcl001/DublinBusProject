import React, {Component} from 'react';
import AppViewFavourAndLogin from "./AppViewFavourAndLogin"
import '../Static/StyleSheet/StyleSearchByStop.css'
import {Link} from 'react-router-dom'

import AppViewHeader from "./AppViewHeader"

//This Component is Search by Stop at the mobile view ports
class SearchByStop extends Component {

    render() {
        return (
            <div className='EntireBox SearchByStop container position-absolute col-md-12 bg-light'
                 id='EntireBox_SearchStop'>

                <AppViewHeader SearchState="Search by Stop Number"/>
                <AppViewFavourAndLogin/>
                <div className='col-12' id='formColor'>

                    <form id='SearchByStopForm'>

                        <label htmlFor="fname">Stop Number : </label>

                        <input type="text"/>
                    </form>
                </div>

                <Link to={'/ResultPage_Stop_Route'}>
                    <button type="button" className="btn btn-warning col-7"
                            id='SubmitButton'>Submit
                    </button>
                </Link>

            </div>
        );
    }

}


export default SearchByStop;
