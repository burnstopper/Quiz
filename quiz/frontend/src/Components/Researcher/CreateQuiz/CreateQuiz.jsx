import React, { Component } from "react";
import "./CreateQuiz.css";
import CookieLib from "../../../cookielib/index";
import axios from "axios";
import LoadingScreen from "react-loading-screen";
import { Spinner } from "react-bootstrap";
import { useParams, Navigate } from "react-router-dom";

let names = {
	name: "Название",
	description: "Описание",
	template_id: "Шаблон",
};

function withParams(Component) {
	return (props) => <Component {...props} params={useParams()} />;
}

class Quiz extends Component {
	constructor(props) {
		super(props);
		this.state = {
			quiz_id: this.props.params.quiz,
			loading: true,
			edit: false,
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

	async getQuizData() {
		let quiz = await axios
			.get(`/api/quizzes/${this.state.quiz_id}`)
			.then((x) => x.data)
			.catch((e) => alert(e.response.statusText));

		if (quiz)
			this.setState({
				name: quiz.name,
				template_id: quiz.template_id,
				description: quiz.description,
				edit: true,
			});
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
					.get(`/api/templates`)
					.then((x) => x.data)
					.catch((e) => alert(e.response.statusText));

				this.setState({ templates, template_id: templates[0]?.id });
			},
		};
		async function start() {
			for (let i of Object.keys(getData)) {
				await getData[i]();
			}
			if (this.state.quiz_id && this.state.quiz_id !== "create")
				await this.getQuizData();
			this.setState({ loading: false });
		}
		start.bind(this)();
	}

	async submit() {
		let unchecked = Object.keys(names).filter(
			(x) => !this.state[x] || this.state[x] === ""
		);
		if (unchecked.length !== 0)
			return alert(
				`Вы не ввели: ${unchecked.map((x) => `${names[x]}`).join(", ")}`
			);
		let data;
		if (!this.state.edit)
			data = await axios
				.post(`/api/quizzes`, {
					name: this.state.name,
					description: this.state.description,
					template_id: this.state.template_id,
				})
				.catch((e) => alert(e.response.statusText));
		else
			data = await axios
				.put(`/api/quizzes`, {
					id: this.state.quiz_id,
					name: this.state.name,
					description: this.state.description,
					template_id: this.state.template_id,
				})
				.catch((e) => alert(e.response.statusText));
		if (data.status === 200)
			window.location.href = `/researcher/info/${data.data.id}`;
		else alert(data.statusText);
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
					<a id="text">
						{this.state.edit ? "Редактирование" : "Создание"} опроса
					</a>
				</div>

				<div id="quizTile">
					<div id="createQuizTile1" className="row">
						<a id="quizText">Название опроса</a>
						<input
							id="search"
							value={this.state.name || ""}
							onChange={(e) => this.setState({ name: e.target.value })}
							type="text"
							placeholder="Write something.."
						/>
					</div>

					<div id="createQuizTile1" className="row">
						<a id="quizText">Описание</a>
						<textarea
							id="descriptionArea"
							value={this.state.description || ""}
							onChange={(e) => this.setState({ description: e.target.value })}
							placeholder="Write something.."
						></textarea>
					</div>
					{/* 
					<div id="createQuizTile1" className="row">
						<a id="quizText">Название группы</a>
						<input
							id="search"
							value={this.state.group}
							onChange={(e) => this.setState({ group: e.target.value })}
							type="text"
							placeholder="Write something.."
						/>
					</div> */}

					<div id="createQuizTile1" className="row">
						<a id="quizText">Шаблон</a>
						<select
							id="select"
							value={this.state.template_id}
							onChange={(e) => this.setState({ template_id: e.target.value })}
						>
							{this.state.templates.map((x) => (
								<option key={x.id} value={x.id}>
									{x.name}
								</option>
							))}
						</select>
					</div>
				</div>

				<div id="downTile">
					<button id="btnPlay" onClick={this.submit.bind(this)}>
						Создать
					</button>
				</div>
			</div>
		) : (
			<Navigate to="/quizzes" replace={true} />
		);
	}
}

export default withParams(Quiz);
