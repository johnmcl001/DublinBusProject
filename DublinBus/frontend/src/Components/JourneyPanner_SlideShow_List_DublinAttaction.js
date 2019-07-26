<<<<<<< HEAD
import React, { Component } from "react";
import SlidingPane from "react-sliding-pane";
import "react-sliding-pane/dist/react-sliding-pane.css";
import "../Static/StyleSheet/SlideShowMobileMap.css";
import Cards from "./JourneyPlanner_Card";

//This the Submit button for the Result page of the Search by Destination
class JourneyPanner_SlideShow_List_DublinAttaction extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isPaneOpen: false,
      isPaneOpenLeft: false
    };
  }

  render() {
    return (
      <div
        className="row container ResultPageButton position-absolute "
        id="JourneyPannerListBottom"
      >
        <div className="col-8 d-lg-none JourneyPannerListButton  ">
          <a
            className="btn btn-warning "
            style={{ width: "auto" }}
            onClick={() => this.setState({ isPaneOpenLeft: true })}
          >
            Show All Attraction
          </a>
        </div>

        <SlidingPane
          className="d-lg-none"
          closeIcon={
            <a>
              <i className="fas fa-arrow-left"></i>
            </a>
          }
          isOpen={this.state.isPaneOpenLeft}
          title="All Dublin Attractions"
          from="right"
          width="100%"
          onRequestClose={() => this.setState({ isPaneOpenLeft: false })}
        >
          <div></div>

          <Cards />
        </SlidingPane>
      </div>
    );
  }
=======
import React, {Component} from "react";
import SlidingPane from 'react-sliding-pane';
import 'react-sliding-pane/dist/react-sliding-pane.css';
import "../Static/StyleSheet/SlideShowMobileMap.css";
import Cards from "./JourneyPlanner_Card";


//This the Submit button for the Result page of the Search by Destination
class JourneyPanner_SlideShow_List_DublinAttaction extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isPaneOpen: false,
            isPaneOpenLeft: false
        };
    }

    render() {
        return (
            <div className="row container ResultPageButton position-absolute " id='JourneyPannerListBottom'>

                <div className="col-8 d-lg-none JourneyPannerListButton  ">
                    <a className="btn btn-warning " style={{width: 'auto'}}
                            onClick={() => this.setState({isPaneOpenLeft: true})}>Show All Attraction
                    </a>
                </div>

                <SlidingPane
                    className='d-lg-none'
                    closeIcon={<a><i
                        className="fas fa-arrow-left"></i></a>}
                    isOpen={this.state.isPaneOpenLeft}
                    title='All Dublin Attractions'
                    from='right'
                    width='100%'
                    onRequestClose={() => this.setState({isPaneOpenLeft: false})}>

                    <div>


                    </div>


                <Cards/>
                </SlidingPane>
            </div>
        );
    }
>>>>>>> JourneyPlanner
}

export default JourneyPanner_SlideShow_List_DublinAttaction;
