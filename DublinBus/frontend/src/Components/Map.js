import React, {Component} from 'react';
import "../static/frontend/stylesheet//Map.css"

class Map extends Component {
    render() {
        return (
            <div id='map '>
                <div className='d-none d-lg-block d-md-none'>
                    <div id="map-container-google-1 " className="z-depth-1-half map-container border border-primary" >
                        <iframe src="https://maps.google.com/maps?q=manhatan&t=&z=13&ie=UTF8&iwloc=&output=embed"
                                frameBorder="0"
                                allowfullscreen></iframe>
                    </div>

                </div>
                {/*<SearchByStop/>*/}
            </div>
        );
    }

}

let mapsyle={


}
export default Map;
