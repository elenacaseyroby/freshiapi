import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
} from 'react-router-dom';
import DesignSystem from './DesignSystem';
import getDevice from './styles/getDevice';
import getFonts from './styles/getFonts';
import getColors from './styles/getColors';

// import logo from './logo.svg';
// import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      windowWidth: 400,
      windowHeight: 600,
      lightMode: true,
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
    const windowWidth = typeof window !== 'undefined' ? window.innerWidth : 400;
    const windowHeight = typeof window !== 'undefined' ? window.innerHeight : 600;
    this.setState({
      windowWidth,
      windowHeight,
    });
  }

  render() {
    const {
      windowWidth,
      windowHeight,
      lightMode,
    } = this.state;
    const device = getDevice(windowWidth);
    const colors = getColors(lightMode);
    const fonts = getFonts(windowWidth);
    const media = {
      windowWidth,
      windowHeight,
      colors,
      device,
      fonts,
      lightMode };
    return (
      <div
      // try to center the entire app like swift
        style={{
          display: 'flex',
          alignSelf: 'center',
          minHeight: windowHeight,
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: colors.background,
        }}
      >
        <Router>
          <Route
            exact
            path="/design-system"
            render={() => (
              <DesignSystem media={media} />
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
      </div>
    );
  }
}

export default App;
