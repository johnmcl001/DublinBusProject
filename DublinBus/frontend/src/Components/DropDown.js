import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

const DropDown = props => {
  const onClick = e => {
    {
      /*
        Input: target element, user click
        Output: parent state and autocomplete updated
    */
    }
    console.log(e.currentTarget.value);
    props.updateState(e.currentTarget.value);
    props.updateAutocomplete(e.currentTarget.value);
  };

  const onKeyDown = e => {
    {
      /*
        Input: target element, user keyboard press
        Output: parent state and autocomplete updated
    */
    }
    if (e.keyCode === 13) {
      props.updateState(e.currentTarget.value);
      props.updateAutocomplete(e.currentTarget.value);
    }
  };

  let optionList;

  if (!props.suggestions) {
  } else {
    console.log(props.suggestions[0]);
    optionList = props.suggestions.map((option, index) => {
      return (
        <option key={index} value={option.direction_id} onClick={onClick}>
          {option.trip_headsign}
        </option>
      );
    });
  }

  return (
    <select
      defaultValue="Direction"
      onClick={onClick}
      onKeyDown={onKeyDown}
      id="dropdown"
    >
      {optionList}
    </select>
  );
};

export default DropDown;
