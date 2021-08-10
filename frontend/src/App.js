import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
} from 'react-router-dom';
import DesignSystem from './components/DesignSystem/DesignSystem';
import getColors from './styles/getColors';
import getFonts from './styles/getFonts';
import PasswordReset from './components/PasswordReset/PasswordReset';

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
    this.toggleLightMode = this.toggleLightMode.bind(this);
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

  toggleLightMode = () => {
    const { lightMode } = this.state;
    this.setState({
      lightMode: !lightMode,
    });
  }

  render() {
    const {
      windowWidth,
      windowHeight,
      lightMode,
    } = this.state;
    const colors = getColors(lightMode);
    const fonts = getFonts(windowWidth);
    // const styles = getStyles(windowWidth);
    const media = {
      windowWidth,
      windowHeight,
      lightMode,
    };
    return (
      <div
      // try to center the entire app like swift
        style={{
          display: 'flex',
          alignSelf: 'center',
          minHeight: windowHeight,
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: colors.background.color,
        }}
      >
        <Router>
          <Route
            exact
            path="/design-system"
            render={() => (
              <DesignSystem media={media} toggleLightMode={this.toggleLightMode} />
            )}
          />
          { /* mobile password reset route with deeplink: */ }
          <Route
            exact
            path="/reset-password/:id/:token"
            render={({ match }) => (
              <PasswordReset
                media={media}
                lightMode={lightMode}
                match={match}
              />
            )}
          />
          <Route
            exact
            path="/"
            render={() => (
              <div style={{
                ...fonts.largeTitle,
                ...colors.interactiveFocus }}
              >
                Freshi
              </div>
            )}
          />
        </Router>
      </div>
    );
  }
}

export default App;
