import React, { Component } from "react";
import data from "../../../data";
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
			data: new data(),
			filter: "",
			group: 1,
			loading: true,
		};
	}

	componentDidMount() {
		let getData = {
			getToken: async () => {
				let token = CookieLib.getCookieToken();
				let id = await axios.get(`token/${token}/id`);
				// let id = "123213121";
				if (!token || !id) {
					token = await axios
						.post("localhost:8001/token/create-respondent")
						.then((x) => x.data)
						.catch(() => {});
					CookieLib.setCookieToken(token);
				}
				this.setState({ token, id });
			},
			getQuizes: async () => {
				let quizes = await axios
					.get("localhost:8001/quizes", {
						params: {
							respondent_id: this.state.id,
							results: true,
							template: true,
						},
					})
					.catch(() => {});

				quizes = quizes.map(async (x) => ({
					...quizes,
					template: await axios
						.get(`localhost:8001/templates/${x.template.id}`)
						.then((x) => x.data),
					results: await axios.get(`localhost:8001/results`, {
						params: { quiz_id: x.quiz_id },
					}),
				}));
				// let quizes = [
				// 	{
				// 		name: "Квиз 1",
				// 		id: 1,
				// 		results: [[], [{}], [{}], []],
				// 		template: { tests: [1, 2, 3] },
				// 	},
				// 	{
				// 		name: "Квиз 2",
				// 		id: 2,
				// 		results: [[], [{}], [{}], []],
				// 		template: { tests: [2, 3] },
				// 	},
				// 	{
				// 		name: "Квиз 3",
				// 		id: 3,
				// 		results: [[{}], [{}], [{}], [{}]],
				// 		template: { tests: [0, 2, 3] },
				// 	},
				// ];
				// console.log(quizes);

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
								to={`${x.quiz_id}`}
								key={i}
							>
								<a id="titleTile">{x.name}</a>
								<a id="descTile">
									{Math.round(
										(x.results.filter(
											(y) =>
												x.template.tests.includes(x.results.indexOf(y)) &&
												y.length > 0
										).length /
											x.template.tests.length) *
											100
									)}
									%
								</a>
							</Link>
						))}
				</div>
				<div id="DownPagination">
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
				</div>
			</div>
		);
	}
}
