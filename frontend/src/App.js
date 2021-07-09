import React, { Component } from 'react';
import getFonts from './styles/getFonts';
// import { BrowserRouter as Router, Route } from 'react-router-dom';

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
    // const media = {
    //   windowWidth,
    // };
    const fonts = getFonts(windowWidth);
    return (
      <div>
        <div style={fonts.largeTitle}>largeTitle</div>
        <div style={fonts.title1}>title1</div>
        <div style={fonts.title2}>title2</div>
        <div style={fonts.title3}>title3</div>
        <div style={fonts.headline}>body</div>
        <div style={fonts.body}>body</div>
        <div style={fonts.callout}>callout</div>
        <div style={fonts.subhead}>subhead</div>
        <div style={fonts.footnote}>footnote</div>
        <div style={fonts.caption1}>caption1</div>
        <div style={fonts.caption2}>caption2</div>
      </div>
    );
  }
}

export default App;
