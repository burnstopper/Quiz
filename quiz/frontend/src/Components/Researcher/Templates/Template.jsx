import React, { Component } from "react";
import "./Template.css";
import CookieLib from "../../../cookielib/index";
import axios from "axios";
import LoadingScreen from "react-loading-screen";
import { Spinner } from "react-bootstrap";
import { Link, Navigate } from "react-router-dom";
import Modal from "react-bootstrap/Modal";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";

let i = 0;
function isBlank(str) {
	return !str || /^\s*$/.test(str);
}

export default class Templates extends Component {
	constructor(props) {
		super(props);
		this.state = {
			filter: "",
			group: 1,
			loading: true,
			isModalOpen: false,
			title: "Опросы",
			list: ["Пусто"],
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

				if (!id) token = await this.createToken();

				this.setState({ token, id }, this.checkPermissions);
			},
			getTemplates: async () => {
				let templates = await axios
					.get("/api/templates", {
						params: {
							// respondent_id: this.state.id
						},
					})
					.then((x) => x.data)
					.catch((e) => alert(e.response.statusText));

				// quizes = quizes.map(async (x) => ({
				// 	...quizes,
				// 	template: await axios
				// 		.get(`/templates/${x.template.id}`)
				// 		.then((x) => x.data),
				// 	results: await axios.get(`/results`, {
				// 		params: { quiz_id: x.quiz_id },
				// 	}),
				// }));
				// let templates = [
				// 	{
				// 		name: "Теплейт 1",
				// 		id: 1,
				// 		tests_ids: [2, 3, 4, 1],
				// 		quizzes: [{ name: "Квиз 1" }],
				// 	},
				// 	{
				// 		name: "Теплейт 3",
				// 		id: 1,
				// 		tests_ids: [2, 3, 4],
				// 		quizzes: [
				// 			{ name: "Квиз 1" },
				// 			{ name: "Квиз 3" },
				// 			{ name: "Квиз 2" },
				// 			{ name: "Квиз 5" },
				// 		],
				// 	},
				// 	{
				// 		name: "Теплейт 2",
				// 		id: 1,
				// 		tests_ids: [2, 4, 1],
				// 		quizzes: [{ name: "Квиз 1" }],
				// 	},
				// ];
				// console.log(templates);

				this.setState({ templates, filtered: templates });
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
				<Modal
					size="lg"
					className="white"
					contentClassName="text-black bg-white"
					show={this.state.isModalOpen}
					onHide={() => this.setState({ isModalOpen: false })}
					aria-labelledby="contained-modal-title-vcenter"
				>
					<Modal.Header closeButton>
						<Modal.Title id="contained-modal-title-vcenter">
							{this.state.title}
						</Modal.Title>
					</Modal.Header>
					<Modal.Body className="show-grid">
						{this.state.list.map((s) => (
							<React.Fragment>
								{s}
								<br />
							</React.Fragment>
						))}
					</Modal.Body>
					<Modal.Footer>
						<Button
							style={{ backgroundColor: "coral" }}
							variant="primary"
							onClick={() => this.setState({ isModalOpen: false })}
						>
							Закрыть
						</Button>
					</Modal.Footer>
				</Modal>

				<div id="upTile">
					<p id="text">Меню шаблонов</p>
					<div className="component-menu">
						<input
							id="search"
							type="text"
							placeholder="Поиск.."
							onChange={(e) => this.setState({ filter: e.target.value })}
						/>

						<button
							type="submit"
							onClick={() =>
								(window.location.href = "/researcher/templates/create")
							}
							id="btnPlays"
						>
							Создать шаблон
						</button>
					</div>
				</div>
				<div id="btnTile">
					{this.state.templates
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

								<div className="quizComponentContainer">
									<button
										onClick={() =>
											this.setState({
												isModalOpen: true,
												title: "Тесты",
												list: x.tests.map((x) => x.name),
											})
										}
										id="quizBtnComponent"
									>
										Тесты
									</button>
									{/* <div className="dropasdasdown"> */}
									<button
										// onClick={() => (window.location.href += `/${x.id}`)}
										onClick={() =>
											this.setState({
												isModalOpen: true,
												title: "Опросы",
												list: x.quizzes.map((x) => x.name),
											})
										}
										id="quizBtnComponentDrop"
									>
										Опросы
									</button>{" "}
									{/* </div> */}
									<button
										onClick={() => (window.location.href = `/quizzes/create`)}
										id="quizBtnComponent"
									>
										Создать опрос
									</button>
									<button
										onClick={() =>
											(window.location.href += `/researcher/templates/${x.id}`)
										}
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
