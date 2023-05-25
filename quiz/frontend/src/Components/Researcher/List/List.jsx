import React, { Component } from "react";
import "./List.css";
import CookieLib from "../../../cookielib/index";
import axios from "axios";
import LoadingScreen from "react-loading-screen";
import { Spinner } from "react-bootstrap";
import { Link, Navigate, useNavigate } from "react-router-dom";

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
			.then((x) => x.data)
			.catch((e) => alert(e.response.statusText));
		CookieLib.setCookieToken(token);
		return token;
	}

	async checkPermissions() {
		let check = await axios
			.get(`/api/token/${this.state.token}/check_researcher`)
			.then((x) => x.data)
			.catch((e) => alert(e.response.statusText));
		// let check = true;
		this.setState({ check });
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
				if (!token) token = await this.createToken();

				this.setState({ token, id }, this.checkPermissions);
			},
			getQuizes: async () => {
				let quizes = await axios
					.get("/api/quizzes")
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
								.get(`/api/results/${x.id}`)
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
		) : this.state.check ? (
			<div className="parent">
				<div id="upTile">
					<p id="text">Меню опросов</p>
					<div className="component-menu">
						<input
							id="search"
							type="text"
							placeholder="Поиск.."
							onChange={(e) => this.setState({ filter: e.target.value })}
						/>

						<button
							onClick={() => (window.location.href = "/researcher/templates")}
							type="submit"
							id="btnPlay"
						>
							Шаблоны
						</button>
						<button
							type="submit"
							onClick={() =>
								(window.location.href = "/researcher/quizzes/create")
							}
							id="btnPlay"
						>
							Создать опрос
						</button>
					</div>
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
								id="btnQuizes"
								style={{ textDecoration: "none" }}
								to={`#`}
								key={i}
							>
								<a id="titleTile">{x.name}</a>
								<a id="descTile">x.invite_link</a>

								<div className="quizComponentContainer">
									<button
										onClick={() =>
											(window.location.href = `/researcher/info/${x.id}`)
										}
										id="quizBtnComponent"
									>
										Открыть
									</button>

									<button
										onClick={() => (window.location.href += `/${x.id}`)}
										id="quizBtnComponent"
									>
										Редактировать
									</button>
								</div>
							</Link>
						))}
				</div>
				{/* <div id="DownPagination">
					<div className="pagination">
						<a href="#">&#10094;</a>
						<a className="active" href="#">
							1
						</a>
						<a href="#">2</a>
						<a href="#">3</a>
						<a href="#">4</a>
						<a href="#">5</a>
						<a href="#">6</a>
						<a href="#">&#10095;</a>
					</div>
				</div> */}
			</div>
		) : (
			<Navigate to="/quizzes" replace={true} />
		);
	}
}
