import ReactDOM from "react-dom";
import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import regeneratorRuntime from "regenerator-runtime";
import Feed from "./Pages/Feed/Feed";
import Login from "./Pages/LoginPage/Login";
import Post from "./Pages/Post/Post";
import Profile from "./Pages/Profile/Profile";
import SignUp from "./Pages/SignUpPage/SignUp";

class App extends Component {
  constructor() {
    super();
    this.state = { isLoggedIn: false };
    this.knowIfLoggedIn = this.knowIfLoggedIn.bind(this);
  }
  UNSAFE_componentWillMount() {
    this.knowIfLoggedIn();
  }
  // Store in state
  async knowIfLoggedIn() {
    await fetch("/api/isLoggedIn", {
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((json) => {
        this.setState({ isLoggedIn: json.result === "True" ? true : false });
      });
  }

  render() {
    return (
      <Router>
        <Switch>
          <Route exact path="/">
            <Feed />
          </Route>
          <Route path="/post/:postId">
            <Post />
          </Route>
          <Route path="/profile/:userId">
            <Profile />
          </Route>

          <Route exact path="/login">
            <Login />
          </Route>
          <Route exact path="/signup">
            <SignUp />
          </Route>
        </Switch>
      </Router>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("app"));
export default App;
