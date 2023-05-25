import React, { Component } from "react";
import "./List.css";
import CookieLib from "../../../cookielib/index";
import axios from "axios";
import LoadingScreen from "react-loading-screen";
import { Spinner } from "react-bootstrap";
import { Link } from "react-router-dom";

let i = 0;
function isBlank(str) {
	return !str || /^\s*$/.test(str);
}

export default class List extends Component {
	constructor(props) {
		super(props);
		this.state = {
			filter: "",
			group: 1,
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

				this.setState({ token, id });
			},
			getQuizes: async () => {
				let quizes = await axios
					.get("/api/quizzes", {
						params: {
							respondent_id: this.state.id,
						},
					})
					.then((x) => x.data)
					.catch((e) => alert(e.response.statusText));

				if (quizes)
					quizes = await Promise.all(
						quizes.map(async (x) => ({
							...x,
							template: await axios
								.get(`/api/templates/${x.template_id}`)
								.then((y) => y.data)
								.catch((e) => alert(e.response.statusText)),
							results: await axios
								.get(`/api/results/${x.id}`, {
									params: {
										respondent_id: this.state.id,
									},
								})
								.then((y) => y.data.tests_result)
								.catch((e) => alert(e.response.statusText)),
						}))
					);

				this.setState({ quizes, filtered: quizes });
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
		return this.state.loading ? (
			<>
				<LoadingScreen
					loading={true}
					bgColor="#E7E2E2"
					spinnerColor="#ff7f50"
					textColor="#676767"
				></LoadingScreen>
				<Spinner animation="border" role="status">
					<span className="sr-only">Loading...</span>
				</Spinner>
			</>
		) : (
			<div className="parent">
				<div id="upTile">
					<p id="text">Доступные опросы</p>
					<input
						id="search"
						type="text"
						placeholder="Поиск.."
						onChange={(e) => this.setState({ filter: e.target.value })}
					/>
				</div>

				<div id="btnTile">
					{this.state.quizes
						.filter((x) =>
							isBlank(this.state.filter)
								? true
								: x.name.toLowerCase().includes(this.state.filter.toLowerCase())
						)
						.map((x, i) => (
							<Link
								id="btnQuiz"
								style={{ textDecoration: "none" }}
								to={`${x.id}`}
								key={i}
							>
								<a id="titleTile">{x.name}</a>
								<a id="descTile">
									{Math.round(
										([...new Set(x.results.map((item) => item.id))].length /
											x.template.tests.length) *
											100
									)}
									%
								</a>
							</Link>
						))}
				</div>
			</div>
		);
	}
}
