import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

const Autocomplete = props => {
  const [activeSuggestion, updateActiveSuggestion] = useState(0);
  const [filteredSuggestions, updateFilteredSuggestions] = useState([]);
  const [showSuggestions, updateShowSuggestions] = useState(false);
  const [userInput, updateUserInput] = useState("");

  const onChange = e => {
    {
      /*
      Input: target element
      Output: parent state and autocomplete updated
    */
    }
    const input = e.currentTarget.value;
    const filteredSuggestions = props.suggestions.filter(
      option => option.toLowerCase().indexOf(input.toLowerCase()) > -1
    );
    updateFilteredSuggestions(filteredSuggestions);
    updateShowSuggestions(true);
    updateUserInput(input);
    props.updateState(e.currentTarget.value);
  };

  const onClick = e => {
    {
      /*
        Input: target element, user click
        Output: parent state and autocomplete updated
    */
    }
    updateActiveSuggestion(0);
    updateFilteredSuggestions([]);
    updateShowSuggestions(false);
    updateUserInput(e.currentTarget.innerText);
    props.updateState(e.currentTarget.innerText);
    props.updateAutocomplete(e.currentTarget.innerText);
  };

  const onKeyDown = e => {
    {
      /*
        Input: target element, user keyboard press
        Output: parent state and autocomplete updated
    */
    }
    if (e.keyCode === 13) {
      updateActiveSuggestion(0);
      updateShowSuggestions(false);
      updateUserInput(filteredSuggestions[activeSuggestion]);
      props.updateState(filteredSuggestions[activeSuggestion]);
      props.updateAutocomplete(filteredSuggestions[activeSuggestion]);
    } else if (e.keyCode === 38) {
      if (activeSuggestion === 0) {
        return;
      }
      updateActiveSuggestion(activeSuggestion - 1);
    } else if (e.keyCode === 40) {
      if (activeSuggestion - 1 === filteredSuggestions.length) {
        return;
      }

      updateActiveSuggestion(activeSuggestion + 1);
    }
  };

  {
    /*
    Suggestion List to be populated as user types
  */
  }
  let suggestionList;

  if (showSuggestions && userInput) {
    if (filteredSuggestions.length) {
      suggestionList = (
        <ul>
          {filteredSuggestions.map((suggestionName, index) => {
            if (index === activeSuggestion) {
            }
            return <li onClick={onClick}>{suggestionName}</li>;
          })}
        </ul>
      );
    } else {
      suggestionList = <p>No options</p>;
    }
  }

  return (
    <div>
      <input
        type="text"
        onChange={e => onChange(e)}
        onClick={e => onClick(e)}
        onKeyDown={e => onKeyDown(e)}
        value={userInput}
      />
      {suggestionList}
    </div>
  );
};

export default Autocomplete;
