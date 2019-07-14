import React, {Component} from 'react';
import '../Static/StyleSheet/AppViewHeader.css'
import DropDownINav from './DropDownNav'

// This Component is a header at the mobile view

class AppViewHeader extends Component {


    render() {

        return (

            <div className='container AppViewHeader '>

                <div className="row ">

                    <div className="col-2 ">
                        {/*Return to previous component */}
                        <a id='returnButton' onClick={() => (window.history.go(-1))}><i
                            className="fas fa-arrow-left"></i></a>
                    </div>

                    <div className="col-8  ccc">

                        <h5>{this.props.SearchState}</h5>
                    </div>

                    <div className="col-2 container  " id='AppViewDropDown'>

                        <DropDownINav/>

                    </div>
                </div>
            </div>
        );
    }

}


export default AppViewHeader;
