import React, { Component } from "react";
import CookieLib from "../../../cookielib/index";
import axios from "axios";
import { useParams } from "react-router-dom";

function withParams(Component) {
	return (props) => <Component {...props} params={useParams()} />;
}

class Quiz extends Component {
	constructor(props) {
		super(props);
		this.state = {
			quiz_id: this.props.params?.quiz,
			loading: true,
		};
	}

	async createToken() {
		let token = await axios
			.post("/api/token/create_respondent")
			.then((x) => x.data.respondent_token)
			.catch((e) => alert(e.response.statusText));
		CookieLib.setCookieToken(token);
		return token;
	}

	async addMember() {
		await axios
			.get(`/invite/quizzes/${this.state.quiz_id}/add`, {
				params: {
					respondent_id: this.state.id,
				},
			})
			.then((x) => x.data)
			.catch((e) => alert(e.response.statusText));
		window.location.href = `/quizzes/${this.state.quiz_id}`;
	}

	componentDidMount() {
		let getData = {
			getToken: async () => {
				let token = CookieLib.getCookieToken();
				if (!token || token === undefined || token === "undefined")
					token = await this.createToken();

				let id = await axios
					.get(`/api/token/${token}/id`)
					.then((x) => x.data.respondent_id)
					.catch((e) => alert(e.response.statusText));

				if (!id) token = await this.createToken();

				this.setState({ token, id }, this.addMember);
			},
		};
		async function start() {
			for (let i of Object.keys(getData)) {
				await getData[i]();
			}
			this.setState({ loading: false });
		}
		start.bind(this)();
	}

	render() {
		return <></>;
	}
}

export default withParams(Quiz);
