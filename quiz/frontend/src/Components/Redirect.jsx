import React, { Component } from "react";
import { Navigate } from "react-router-dom";

export default class Templates extends Component {
	render() {
		return <Navigate to="/quizes" replace={true} />;
	}
}
