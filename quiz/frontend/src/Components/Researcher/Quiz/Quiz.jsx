import React, { Component } from "react";
import data from "../../../data";
import "./Quiz.css";
import CookieLib from "../../../cookielib/index";
import LoadingScreen from "react-loading-screen";
import { Spinner } from "react-bootstrap";
import { Link, Navigate } from "react-router-dom";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import { Draggable, Droppable } from "react-drag-and-drop";
import Dropdown from "react-bootstrap/Dropdown";
import Accordion from "react-bootstrap/Accordion";
import axios from "axios";
let i = 0;
function isBlank(str) {
	return !str || /^\s*$/.test(str);
}

function array_move(arr, old_index, new_index) {
	if (new_index >= arr.length) {
		var k = new_index - arr.length + 1;
		while (k--) {
			arr.push(undefined);
		}
	}
	arr.splice(new_index, 0, arr.splice(old_index, 1)[0]);
	return arr; // for testing
}

export default class Templates extends Component {
	constructor(props) {
		super(props);
		this.state = {
			data: new data(),
			group: 1,
			loading: true,
			isModalOpen: false,
			title: "Опросы",
			list: ["Пусто"],
		};
	}

	handleDrop(data, index) {
		let array = Array.from(this.state.template.tests_ids);
		// let tmp = array[data.tests];
		let result = array_move(array, data.tests, index);
		// array[data.tests] = array[this.index];
		// array[this.index] = tmp;
		let template = this.state.template;
		template.tests_ids = result;
		this.setState({ template });
		console.log(this.state.template);
	}

	async createToken() {
		let token = await axios
			.post("localhost:8001/api/token/create_respondent")
			.then((x) => x.data)
			.catch(() => {});
		CookieLib.setCookieToken(token);
		return token;
	}

	componentDidMount() {
		let getData = {
			getToken: async () => {
				let token = CookieLib.getCookieToken();
				// let id = "123213121";
				if (!token) token = await this.createToken();

				let id = await axios
					.get(`localhost:8001/api/token/${token}/id`)
					.then((x) => x.data);
				if (!token) token = await this.createToken();

				this.setState({ token, id });
			},
			checkPermission: async () => {
				// let check = await axios
				// 	.get(`/token/${this.state.quiz_id}/check_researcher`)
				// 	.then((x) => x.data);
				let check = true;
				this.setState({ check });
			},
			getQuiz: async () => {
				let quiz = await axios
					.get(`localhost:8001/api/quizes/${this.state.quiz_id}`, {
						params: {
							respondent_id: this.state.id,
							results: true,
							template: true,
						},
					})
					.catch(() => {});
				quiz = {
					...quiz,
					template: await axios
						.get(`localhost:8001/api/templates/${quiz.template.id}`)
						.then((x) => x.data),
					results: await axios.get(`localhost:8001/api/results`, {
						params: { quiz_id: quiz.quiz_id },
					}),
				};
				// let quiz = {
				// 	name: "Квиз 2",
				// 	description: "Опрос для БКНАД 211 и БКНАД 212, всем хорошего дня",
				// 	template: { tests: [0, 3, 2] },
				// 	results: [[{}], [{}], [{}], []],
				// };

				this.setState({ quiz });
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
				<div class="container">
					<Accordion id="accord-block" defaultActiveKey="0">
						<Accordion.Item id="accord-item" eventKey="0">
							<Accordion.Header>Название</Accordion.Header>
							<Accordion.Body>
								Кол-во участников <br /> Участник (63%) 1 <br /> Участник 2 (0%)
							</Accordion.Body>
						</Accordion.Item>
					</Accordion>
					<Accordion id="accord-block" defaultActiveKey="0">
						<Accordion.Item id="accord-item" eventKey="0">
							<Accordion.Header>Ссылка</Accordion.Header>
							<Accordion.Body id="accord-text">
								Кол-во участников <br /> Участник (63%) 1 <br /> Участник 2 (0%)
							</Accordion.Body>
						</Accordion.Item>
					</Accordion>
				</div>
				<div className="calendar"></div>
			</div>
		) : (
			<Navigate to="/quizes" replace={true} />
		);
	}
}