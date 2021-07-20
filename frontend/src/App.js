import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
} from 'react-router-dom';
import DesignSystem from './DesignSystem/DesignSystem';
import FreshiButton from './components/FreshiButton';
import getColors from './styles/getColors';
import getFonts from './styles/getFonts';
import getStyles from './styles/getStyles';

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
    const styles = getStyles(windowWidth);
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
          { /* mobile password reset route: */ }
          <Route
            exact
            path="/reset-password/:id/:token"
            render={({ match }) => {
              const { id, token } = match.params;
              const host = 'www.freshi.io';
              // const host = 'localhost:8000';
              const currentRoute = `${host}/${id}/${token}`;
              const deeplink = `freshi://${host}/reset-password?userId=${id}&authToken=${token}`;
              window.location = deeplink;
              return (
                <div style={{
                  display: 'block',
                  ...styles.padding }}
                >
                  <div style={{
                    ...fonts.largeTitle,
                    ...colors.interactiveFocus }}
                  >
                    Freshi
                  </div>
                  <br />
                  <div style={{
                    ...fonts.headline,
                    ...colors.highContrast }}
                  >
                    To reset your password:
                  </div>
                  <div style={{
                    ...fonts.body,
                    ...colors.highContrast }}
                  >
                    <br />
                    1. Download the Freshi app on your iPhone or tablet.
                    <br />
                    2. Open the Freshi app on your iPhone or tablet.
                    <br />
                    3. On the same device, go to this url: &nbsp;
                    <br />
                    <div style={{
                      ...styles.marginTop,
                      ...styles.marginBottom
                    }}
                    >
                      <FreshiButton
                        label="visit url"
                        onClick={() => {
                          window.location.href = currentRoute;
                        }}
                        backgroundColor={colors.background.color}
                        forgroundColor={colors.interactiveFocus.color}
                        media={media}
                        style={{
                          ...styles.marginRight
                        }}
                      />
                      <FreshiButton
                        label="copy url"
                        onClick={() => {
                          navigator.clipboard.writeText(currentRoute);
                        }}
                        backgroundColor={colors.interactiveFocus.color}
                        forgroundColor={colors.background.color}
                        media={media}
                      />
                    </div>
                    <br />
                    4. Reset your password and enjoy!
                    <br />
                    <br />
                    If you still can&apos;t access your account,
                    <br />
                    send me an email and I&apos;ll be happy to help you out!
                    <br />
                    <div style={{
                      ...styles.marginTop,
                      ...styles.marginBottom
                    }}
                    >
                      <FreshiButton
                        label="send email"
                        onClick={() => {
                          window.location.href = 'mailto: casey@freshi.io';
                        }}
                        backgroundColor={colors.background.color}
                        forgroundColor={colors.interactiveFocus.color}
                        media={media}
                        style={{
                          ...styles.marginRight,
                        }}
                      />
                      <FreshiButton
                        label="copy email"
                        onClick={() => {
                          navigator.clipboard.writeText('casey@freshi.io');
                        }}
                        backgroundColor={colors.interactiveFocus.color}
                        forgroundColor={colors.background.color}
                        media={media}
                      />
                    </div>
                  </div>
                </div>
              );
            }}
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
