// src/CongressionalDistricts.js

import React, { Component } from 'react';
import * as topojson from 'topojson';
import * as d3 from 'd3v4';


class CongressionalDistricts extends Component {
    state = {
        usData: null,
        usCongress: null
    }

    componentWillMount() {
        d3.queue()
            .defer(d3.json, "us.json")
            .defer(d3.json, "us-congress-113.json")
            .await((error, usData, usCongress) => {
                this.setState({
                    usData,
                    usCongress
                })
            })

    }

    componentDidUpdate() {
        const svg = d3.select(this.refs.anchor)

        const { width, height } = this.props;
        // console.log('width', width)
        // console.log('height', height)

        const projection = d3.geoAlbers()
            .scale(1280)
            .translate([width / 2, height / 2]);
        // console.log('projection', projection)

        const path = d3.geoPath()
            .projection(projection);
        // console.log('path', path)

        const us = this.state.usData
        // console.log('usData', us)

        const congress = this.state.usCongress;
        // console.log('congressData', congress)

        svg.append("defs").append("path")
            .attr("id", "land")
            .datum(topojson.feature(us, us.objects.land))
            .attr("d", path);

        svg.append("clipPath")
            .attr("id", "clip-land")
            .append("use")
            .attr("xlink:href", "#land");

        svg.append("g")
            .attr("class", "districts")
            .attr("clip-path", "url(#clip-land)")
            .selectAll("path")
            .data(topojson.feature(congress, congress.objects.districts).features)
            .enter().append("path")
            .attr("d", path)
            .append("title")
            .text(function (d) { return d.id; });

        svg.append("path")
            .attr("class", "district-boundaries")
            .datum(topojson.mesh(congress, congress.objects.districts, function (a, b) { return a !== b && (a.id / 1000 | 0) === (b.id / 1000 | 0); }))
            .attr("d", path);

        svg.append("path")
            .attr("class", "state-boundaries")
            .datum(topojson.mesh(us, us.objects.states, function (a, b) { return a !== b; }))
            .attr("d", path);
    }

    render() {
        const { usData, usCongress } = this.state;
        // console.log(usData)
        // console.log(usCongress)

        if (!usData || !usCongress) {
            return null;
        }

        return <g ref="anchor" />;
    }
}

export default CongressionalDistricts;