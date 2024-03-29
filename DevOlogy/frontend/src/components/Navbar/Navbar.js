import {
  faComments, faHome, faPlus, faUser
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { Component } from "react";
import { syncFetchRequest } from "../../../helpers/fetchRequest";
import "./Navbar.css";

const searchInputPlaceholder = "Search";


const activeColour = "black";
const normalColour = "gray";

export default class Navbar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      requestUserData: this.getRequestUserInfo(),
      searchValue: "",
      searchPlaceholder: searchInputPlaceholder,
      cancelOnBlur: true,
      searchDiv: null,
      isMouseInside: false,
      searchResults: {},
      showSearchHere: true,
      isActivityActive: window.location.pathname.startsWith("/activity"),
      isExploreActive: window.location.pathname.startsWith("/explore"),
      isHomeActive: window.location.pathname === "/",
      isMessengerActive: window.location.pathname.startsWith("/chat"),
      isProfileActive: window.location.pathname.startsWith("/profile"),
    };
  }
  getSearchResults = async () => {
    syncFetchRequest({
      path_: "/api/general/getSearchResults/",
      method: "POST",
      body: {
        query: this.state.searchValue,
      },
      next: (data) => {
        this.setState(
          { searchResults: data.response.response },
          this.renderSearchResults
        );
      },
    });
  };
  getRequestUserInfo = async () => {
    syncFetchRequest({
      path_: "/api/user/getRequestUserInfo/",
      method: "POST",
      next: (data)=>{
        this.setState({ requestUserData: data.response }, () => {
          this.props.setUserData(data.response);
        });
        return data.response;
      }
    })
    
  };
  renderSearchResults = () => {};
  componentDidMount() {
    this.setState({ searchDiv: document.getElementById("srchResults") });
    window.addEventListener("click", 
    ()=>{
      if (!this.state.isMouseInside) {
        this.state.searchDiv.style.display = "none";
      }
    });
  }
  handleSearchOnChange = (e) => {
    if (document.getElementById("results").innerHTML === "") {
      this.setState({ showSearchHere: true });
    } else {
      this.setState({ showSearchHere: false });
    }
    this.setState({ searchValue: e.target.value }, () => {
      this.getSearchResults();
    });
  };
  handleSearchOnFocus = () => {
    this.setState({ searchPlaceholder: "" });
    this.state.searchDiv.style.display = "block";
  };
  handleSearchOnBlur = () => {
    if (this.state.searchValue.length === 0) {
      this.setState({
        searchPlaceholder: searchInputPlaceholder,
        searchResults: {},
      });
    } else {
      this.setState({ searchPlaceholder: this.state.searchValue });
    }

    if (!this.state.isMouseInside) {
      this.state.searchDiv.style.display = "none";
    }
  };
  render() {
    return (
      <>
        <nav>
          <div className="leftNav">
            <a href="/">
              <img src="/static/images/written-logo.png" alt="" />
            </a>
          </div>
          <div className="centerNav">
            <input
              type="text"
              value={this.state.searchValue}
              onChange={this.handleSearchOnChange}
              placeholder={this.state.searchPlaceholder}
              onFocus={this.handleSearchOnFocus}
              onBlur={this.handleSearchOnBlur}
              onMouseLeave={() => this.setState({ isMouseInside: false })}
            onMouseEnter={() => this.setState({ isMouseInside: true })}
            />
          </div>
          <div className="rightNav">
            <div className="icon-div">
              {/* <img className="icon" src="/static/svgs/home.png" alt="" /> */}
              <FontAwesomeIcon
                icon={faHome}
                color={this.state.isHomeActive ? activeColour : normalColour}
                size={"lg"}
              />
            </div>
            <div className="icon-div">
              {/* <img className="icon" src="/static/svgs/messenger.png" alt="" /> */}
              <FontAwesomeIcon
                icon={faComments}
                color={
                  this.state.isMessengerActive ? activeColour : normalColour
                }
                size={"lg"}
              />
            </div>
            <div className="icon-div">
            <FontAwesomeIcon
                icon={faPlus}
                color={
                  this.state.isMessengerActive ? activeColour : normalColour
                }
                size={"lg"}
              />
            </div>
            {/* <div className="icon-div">
              <img className="icon" src="/static/svgs/compass.png" alt="" />
              <FontAwesomeIcon
                icon={faCompass}
                color={this.state.isExploreActive ? activeColour : normalColour}
                size={"lg"}
              />
            </div> */}
            {/* <div className="icon-div">
              <img className="icon" src="/static/svgs/heart.svg" alt="" />
              <FontAwesomeIcon
                icon={faHeart}
                color={
                  this.state.isActivityActive ? activeColour : normalColour
                }
                size={"lg"}
              />
            </div> */}
            <div className="icon-div">
              {/* <img
                className="icon"
                src={this.state.requestUserData.dp_url}
                alt=""
              /> */}
              {this.state.requestUserData.dp_url === "/static/svgs/user.png" ? (
                <FontAwesomeIcon
                  icon={faUser}
                  color={
                    this.state.isProfileActive ? activeColour : normalColour
                  }
                  size={"lg"}
                />
              ) : (
                <img
                  className="icon"
                  id="dp-icon"
                  src={this.state.requestUserData.dp_url}
                  alt=""
                />
              )}
            </div>
          </div>
        </nav>

        <div
          className="container flex-h-center"
          id="srchResults"
          style={{ display: "none", textAlign: "center" }}
          onMouseLeave={() => this.setState({ isMouseInside: false })}
          onMouseEnter={() => this.setState({ isMouseInside: true })}
        >
          <div className="header">
            {this.state.showSearchHere ? <b>Search Here</b> : ""}
          </div>
          <div id="results">
            {Object.keys(this.state.searchResults).length > 0
              ? Object.keys(this.state.searchResults).map((key) => (
                  <a
                    className="link"
                    href={"/profile" + this.state.searchResults[key].link + "/"}
                    key={this.state.searchResults[key].username}
                  >
                    <div className="rectangle row">
                      <div className="dp col-2">
                        <img
                          className="searchImage"
                          src={this.state.searchResults[key].image}
                          alt={this.state.searchResults[key] + "'s image"}
                        />
                      </div>

                      <div className="name col-8">
                        <div className="container name-upper">
                          {this.state.searchResults[key].username}
                        </div>
                        <div className="container name-lower">
                          {this.state.searchResults[key].full_name}
                        </div>
                      </div>
                    </div>
                  </a>
                ))
              : "No Results Found"}
          </div>
        </div>
      </>
    );
  }
}
