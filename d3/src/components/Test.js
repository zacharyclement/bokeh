import React, { Component } from 'react';
import * as d3 from 'd3v4';

class Test extends Component {
    state = {
        testData: null,
    }

    componentWillMount() {
        d3.queue()
            .defer(d3.json, "testData.json")
            .await((error, testData) => {
                this.setState({
                    testData,
                })
            })

    }

    componentDidUpdate() {

        const { width, height } = this.props;

        const bardata = this.state.testData.bardata

        const svg = d3.select(this.refs.anchor)

        // console.log('this.state', this.state.testData.data)

        svg.append('rect')
            .attr('x', 200)
            .attr('y', 100)
            .attr('height', 200)
            .attr('width', 200)
            .style('fill', 'red')

        svg.selectAll('rect')
            .data(bardata)
            .enter()
            .append('rect')
            .style('fill', 'black')
            .attr('width', 20)
            .attr('height', function (d) {
                // console.log('d', d)
                return d;
            })
            .attr('x', function (d, i) {
                return i * (20 + 20);
            })
            .attr('y', function (d) {
                return 400 - d;
            });
    }

    render() {
        const { testData } = this.state;
        // console.log(testData)

        if (!testData) {
            return null;
        }

        return <g ref="anchor" />;
    }
}

export default Test;