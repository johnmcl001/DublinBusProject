import React, {Component} from 'react';
import {FaBeer} from 'react-icons/fa';
import AppViewFavourAndLogin from "./AppViewFavourAndLogin"
import '../static/frontend/stylesheet/StyleSearchByStop.css'

import AppViewHeader from "./AppViewHeader"

class SearchByStop extends Component {
    render() {
        return (
            <div className='SearchByStop container position-absolute' id='EntireBox'>
                <div className='col-md-12 col-lg-5 col-xl-4 bg-light  ' id='innerContainer'>
                    <AppViewHeader/>
                    <AppViewFavourAndLogin/>
                    <div className='col-12' id='formColor'>

                        <form id='SearchByStopForm'>

                            <label htmlFor="fname">Stop Number : </label>

                            <input type="text"/>
                        </form>
                    </div>

                    <button type="button" className="btn btn-warning col-7" id='SubmitButton'>Submit</button>

                </div>
            </div>
        );
    }

}


export default SearchByStop;
