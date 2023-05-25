import React, { Component } from "react";
import "./Quiz.css";
import CookieLib from "../../../cookielib/index";
import LoadingScreen from "react-loading-screen";
import { Spinner } from "react-bootstrap";
import { useParams, Navigate } from "react-router-dom";
import Accordion from "react-bootstrap/Accordion";
import axios from "axios";

function withParams(Component) {
	return (props) => <Component {...props} params={useParams()} />;
}
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

export default withParams(
	class Templates extends Component {
		constructor(props) {
			super(props);
			this.state = {
				group: 1,
				quiz_id: this.props.params.quiz,
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
					// let id = "123213121";
					if (!token || token === undefined || token === "undefined")
						token = await this.createToken();

					let id = await axios
						.get(`/api/token/${token}/id`)
						.then((x) => x.data)
						.catch((e) => alert(e.response.statusText));
					if (!token) token = await this.createToken();

					this.setState({ token, id }, this.checkPermissions);
				},
				checkPermission: async () => {
					let check = await axios
						.get(`/token/${this.state.quiz_id}/check_researcher`)
						.then((x) => x.data)
						.catch((e) => alert(e.response.statusText));
					// let check = true;
					this.setState({ check });
				},
				getQuiz: async () => {
					let quiz = await axios
						.get(`/api/quizzes/${this.state.quiz_id}`, {
							params: {
								respondent_id: this.state.id,
							},
						})
						.then((x) => x.data)
						.catch((e) => alert(e.response.statusText));

					if (quiz)
						quiz = {
							...quiz,
							template: await axios
								.get(`/api/templates/${quiz.template_id}`)
								.then((x) => x.data)
								.catch((e) => alert(e.response.statusText)),
							results: await axios
								.get(`/api/results/${quiz.id}`)
								.then((x) => x.data.tests_result)
								.catch((e) => alert(e.response.statusText)),
							respondents: await axios
								.get(`/api/quizzes/${quiz.id}/respondents`)
								.then((x) => x.data.respondents)
								.catch((e) => alert(e.response.statusText)),
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
			) : this.state.check && this.state.quiz?.name ? (
				<div className="parent">
					<div className="container">
						<Accordion id="accord-block" defaultActiveKey="0">
							<Accordion.Item id="accord-item" eventKey="0">
								<Accordion.Header>{this.state.quiz.name}</Accordion.Header>
								<Accordion.Body>
									Кол-во участников: {this.state.quiz.respondents.length} <br />
									{this.state.quiz.respondents
										.map((x) => {
											let results = this.state.quiz.results.filter(
												(y) => y.respondent_id === x
											);

											let res = Math.round(
												([...new Set(results.map((item) => item.id))].length /
													this.state.template.tests.length) *
													100
											);

											return (
												<>
													{x} ({res}%) <br />
												</>
											);
										})
										.join(`\n`)}
								</Accordion.Body>
							</Accordion.Item>
						</Accordion>
						<Accordion id="accord-block" defaultActiveKey="0">
							<Accordion.Item id="accord-item" eventKey="0">
								<Accordion.Header>
									{this.state.quiz.invite_link}
								</Accordion.Header>
								<Accordion.Body id="accord-text">
									{this.state.quiz.description}
								</Accordion.Body>
							</Accordion.Item>
						</Accordion>
					</div>
					<div className="calendar"></div>
				</div>
			) : (
				<Navigate to="/quizzes" replace={true} />
			);
		}
	}
);
