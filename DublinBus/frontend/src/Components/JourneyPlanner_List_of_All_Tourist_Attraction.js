import React, { Component } from "react";
import Cards from "./JourneyPlanner_Card";

class JourneyPlanner_List_of_All_Tourist_Attraction extends Component {
  render() {
    return (
      <React.Fragment>
        {this.props.ListOfAllAttractions.map((cardInfo, Index) => (
          <Cards
            key={cardInfo.id}
            name={cardInfo.name}
            img={cardInfo.img}
            description={cardInfo.description}
            buttonID={`CardButton_${Index}`}
            cardID={`CardAttraction_${Index}`}
            AddAttactionCardFunction={this.props.AddAttactionCardFunction.bind(
              this
            )}
          />
        ))}
      </React.Fragment>
    );
  }
}

export default JourneyPlanner_List_of_All_Tourist_Attraction;
