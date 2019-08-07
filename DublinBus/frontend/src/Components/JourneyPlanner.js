import React, {Component} from "react";
import {Link} from "react-router-dom";
import "../Static/StyleSheet/SearchbyDestination.css";
import "../Static/StyleSheet/JourneyPlanner.css"
import AppViewHeader from "./AppViewHeader";
import AppViewFavourAndLogin from "./AppViewFavourAndLogin";
import YourLocationOrSearch from "./YourLocationOrSearch";
import JouneryPlanner_ToVisitPiont from "./JouneryPlanner_ToVisitPiont";
import JourneyPanner_SlideShow_List_DublinAttaction from './JourneyPanner_SlideShow_List_DublinAttaction';
import JourneyPlanner_List_of_All_Tourist_Attraction from './JourneyPlanner_List_of_All_Tourist_Attraction'
import axios from "axios"
import WarningAlert from './WarningAlert'
import {Button, Accordion, Card} from 'react-bootstrap';
import { addDays } from 'date-fns';
import 'bootstrap';
import * as $ from "jquery";

// npm install react-datepicker --save
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";


//This Component is Search by Destination at the mobile view ports
class JourneyPlanner extends Component {
    constructor(props) {
        super(props);

        this.state = {
            initial_Date: null,
            initial_Time: null,

            startDateToBackEnd: null,
            startTimeToBackEnd: null,

            //Location Co-Ordinate start Here
            currentLocation_lat: null,
            currentLocation_long: null,

            startLat: '',
            startLon: null,
            home: null,

            PickedTouristAttraction: [],
            ListOfAllAttractions: [],
            submittedAttractions: [],

            bgColor: [
                '#F65314',
                '#7CBB00',
                '#00A1F1',
                '#FFBB00',
                '#146EB4',
            ],

            warningText: '',
        };
        this.handleChangeDate = this.handleChangeDate.bind(this);
        this.handleChangeTime = this.handleChangeTime.bind(this);

        this.updateCurrentPosition = this.updateCurrentPosition.bind(this);
        this.updateHome = this.updateHome.bind(this);

        this.setPosition = this.setPosition.bind(this);
        this.ToRemoveSelectedCardsFromListOfAllTouristCard_AfterSelect = this.ToRemoveSelectedCardsFromListOfAllTouristCard_AfterSelect.bind(this)
    }

    checkEmpty() {
        {
            //    To activate Warning alert
        }
        if (this.state.startLat.length == 0) {

            this.setState({
                warningText: 'Hey Please Pick Your Start Point'
            });

            let $ = jQuery;

            (function ($) {
                $('#JourneyPlannerWarning').modal('toggle')
            })(jQuery);


        } else if (this.state.PickedTouristAttraction.length == 0) {

            this.setState({
                warningText: 'Hey Please select some location to visit'
            });
            let $ = jQuery;

            (function ($) {
                $('#JourneyPlannerWarning').modal('toggle')
            })(jQuery);

        } else {

            this.props.history.push(`/JourneyPlannerResultPage/${this.state.startLat}/${this.state.startLon}/${this.state.startDateToBackEnd}/${this.state.startTimeToBackEnd}/${this.state.submittedAttractions}/${this.state.home}`);
        }
    }

    updateHome(newHome) {
        this.setState({
            home: newHome
        })
    }

    componentDidMount() {
        {
            //Fetch list of attractions from server
        }

        axios({
            method: "get",
            url: "http://csi420-01-vm9.ucd.ie/api/attractions/",
            params: {
                route: this.state.routeNumber,
                direction: this.state.direction
            }
        })
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({placeholder: "Something went wrong"});
                }
                {
                    console.log("here");
                }
                return response.data;
            })
            .then(data => this.setState({ListOfAllAttractions: data, loaded: true}));
    }


    updateCurrentPosition(e) {
        this.setState({
            startLat: e.latitude,
            startLon: e.longitude,
            home: e.address
        });
    }


    handleChangeDate(date) {
        //set date
        this.setState({
            initial_Date: date,
            startDateToBackEnd:
                date.getDate() + "-" + (date.getMonth() + 1) + "-" + date.getFullYear()
        });
    }

    handleChangeTime(Time) {
        //set time
        this.setState({
            initial_Time: Time,
            startTimeToBackEnd: Time.getHours() + ":" + Time.getMinutes()
        });
    }


    setPosition(position) {
        {
            //This is Geolocation ask for current location
        }
        this.setState({
            currentLocation_lat: position.coords.latitude,
            currentLocation_long: position.coords.longitude
        });
    }


    ToRemoveSelectedCardsFromListOfAllTouristCard_AfterSelect(attraction) {

        {
            //    This Function is used to remove the card from List of all cards once it been add to to visit list
        }

        this.setState((prevState => ({
                ListOfAllAttractions: prevState.ListOfAllAttractions.filter(el => el.name != attraction.name)
            }))
        );
    }

    AddAttactionCard(attractions) {
        {
            //    This function is for add card from the listed of Tourist Attraction into tourist to visit point components
        }
        console.log(this.state.PickedTouristAttraction)
        if (this.state.PickedTouristAttraction.length <= 4) {
            this.setState({
                    PickedTouristAttraction: [...this.state.PickedTouristAttraction, attractions],


                }, () => {
                    this.ToRemoveSelectedCardsFromListOfAllTouristCard_AfterSelect(attractions)


                },
            )
        } else {
            //This is used to activate the alert box
            let $ = jQuery;

            (function ($) {
                $('#JourneyPlannerAlertBox').modal('toggle')
            })(jQuery);


        }
        this.state.submittedAttractions.push(attractions.name)
    }


    ToAddCardBackToAllCardList(attractions) {
        {
            //    return the card back to all attraction card list after user that card from selected list
        }

        this.setState({
                ListOfAllAttractions: [...this.state.ListOfAllAttractions, attractions],

            }
        )

    }

    removeAttractionFromSelected(attraction) {
        this.setState(prevState => ({
                    PickedTouristAttraction: prevState.PickedTouristAttraction.filter(el => el.name != attraction.name)
                }

            ), () => {
                this.ToAddCardBackToAllCardList(attraction)
            }
        );
        delete this.state.submittedAttractions[this.state.submittedAttractions.indexOf(attraction.name)]
        console.log("jjj")
    }


//    The two function below is used for managing button color (each selected attraction) for Picked Attraction
    _removeSelectedColorFromList(color) {
        {
            //    Remove color from list
        }

        this.setState(prevState => ({
                bgColor: prevState.bgColor.filter(el => el != color)
            }), () => this._AddBackSelectedColor(color)
        )
    }


    _AddBackSelectedColor(color) {
        {
            // re-append the color to end of the list
        }
        this.setState({bgColor: [...this.state.bgColor, color],}
        )
    }

    //End here - managing button color (each selected attraction) for Picked Attraction


    render() {
        console.log(this.state.address_name)

        return (
            <div>

                <div
                    className="EntireBox  SearchByDestinationBox JoureyPlaner bg-light container col-md-12  position-absolute  ">

                    <AppViewHeader
                        SearchState={"Journey Planner"}
                        Return="toHomePage"
                    />
                    <AppViewFavourAndLogin/>

                    <div id="formColor">
                        <form>
                            <div className="container  SearchByDestinationForm">

                                <div className="row  JourneyPlannerRowSecond">
                                    {/*Start location starts here*/}
                                    <div className="col-12 JourneyPlanerAddressLabel ">
                                        <label> Start Point:</label>
                                    </div>

                                    <div className="col-10 JourneyPlanerInput ">
                                        <YourLocationOrSearch
                                            onUpdatePosition={this.updateCurrentPosition}
                                            id='AddressAutoStart'
                                        />
                                    </div>
                                    {/*Start location Ends here*/}
                                </div>

                                {/*The date and time picker starts here*/}
                                <div className='row JoureyPlanerTimeLabel '>
                                    <div className='col-6'><label> Date: </label></div>
                                    <div className='col-6'><label> Time:</label></div>

                                </div>

                                <div className="row row_fifth ">

                                    <div className="col-6  ">
                                        <DatePicker
                                            selected={this.state.initial_Date}
                                            onChange={this.handleChangeDate}
                                            placeholderText="Today"
                                            minDate={new Date()}
                                            maxDate={addDays(new Date(), 9)}
                                        />
                                    </div>
                                    <div className="col-6 ">
                                        <DatePicker
                                            selected={this.state.initial_Time}
                                            onChange={this.handleChangeTime}
                                            showTimeSelect
                                            showTimeSelectOnly
                                            timeIntervals={15}
                                            dateFormat="h:mm aa"
                                            timeCaption="Time"
                                            placeholderText="Now"
                                        />
                                    </div>

                                    {/*The date and time picker Ends here*/}
                                </div>

                                {/*List of Tourist To visit Location  */}
                                <div className="col-12 listDestination_label  ">
                                    <label> Picked Attraction:</label>
                                </div>
                                <div className="accordion" id="accordionExample">
                                    <div className='row listDestination border border-white '>
                                        {/*add to travel destination*/}

                                        {this.state.PickedTouristAttraction.map((cardInfo, index) =>
                                            <JouneryPlanner_ToVisitPiont
                                                ref={this.getFunctionFromToVistPiont}
                                                buttonID={`button_${index}`}
                                                cardID={`attraction_${index}`}
                                                key={index}
                                                name={cardInfo.name} img={cardInfo.img}
                                                description={cardInfo.description}

                                                removeAttractionFromSelected={this.removeAttractionFromSelected.bind(this)}

                                                PickedAttractionButtonBgColor={this.state.bgColor[index]}
                                                _AddBackSelectedColor={this._removeSelectedColorFromList.bind(this)}
                                            />)}

                                    </div>

                                </div>
                                <Accordion>


                                    <JourneyPanner_SlideShow_List_DublinAttaction
                                        AddAttactionCardFunction={this.AddAttactionCard.bind(this)}
                                        ListOfAllAttractions={this.state.ListOfAllAttractions}/>

                                </Accordion>


                            </div>


                        </form>
                    </div>




                        <button
                            type="button"
                            className="btn btn-warning col-7"
                            id="SubmitButton"
                            onClick={this.checkEmpty.bind(this)}
                        >
                            Submit
                        </button>




                </div>


                <Accordion className="ListofAllAttractions d-none d-lg-block ">

                    <JourneyPlanner_List_of_All_Tourist_Attraction
                        AddAttactionCardFunction={this.AddAttactionCard.bind(this)}
                        ListOfAllAttractions={this.state.ListOfAllAttractions}


                    />


                </Accordion>

                   <WarningAlert color={'#146EB4'} id={'JourneyPlannerAlertBox'} title={'Information'}
                              content={'Sorry, You can only select five attraction.'}

                />
                <WarningAlert color={'#F65314'} id={'JourneyPlannerWarning'} title={'Warning'}
                              content={this.state.warningText}

                />


            </div>
        );
    }
}

export default JourneyPlanner;
