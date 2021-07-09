import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import DesignSystem from './DesignSystem';

// import logo from './logo.svg';
// import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      windowWidth: 0,
    };
    this.updateDimensions = this.updateDimensions.bind(this);
  }

  componentDidMount() {
    this.updateDimensions();
    window.addEventListener('resize', this.updateDimensions);
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.updateDimensions);
  }

  updateDimensions = () => {
    const windowWidth = typeof window !== 'undefined' ? window.innerWidth : 0;
    this.setState({
      windowWidth,
    });
  }

  render() {
    const {
      windowWidth,
    } = this.state;
    return (
      <Router>
        <Route
          exact
          path="/design-system"
          render={() => (
            <DesignSystem windowWidth={windowWidth} />
          )}
        />
        <Route
          exact
          path="/"
          render={() => (
            <></>
          )}
        />
      </Router>
    );
  }
}

export default App;
