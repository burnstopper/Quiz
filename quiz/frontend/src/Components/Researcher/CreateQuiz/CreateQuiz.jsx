import React, { Component } from "react";
import data from "../../../data";
import "./CreateQuiz.css";
import CookieLib from "../../../cookielib/index";
import axios from "axios";
import LoadingScreen from "react-loading-screen";
import { Spinner } from "react-bootstrap";
import { Link } from "react-router-dom";
import { useParams, Navigate } from "react-router-dom";

const tests = [
	{
		name: "Какой-то там первый",
		link: "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
	},
	{
		name: "Второй",
		link: "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
	},
	{
		name: "Третий",
		link: "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
	},
	{
		name: "Четвертый",
		link: "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
	},
];

function withParams(Component) {
	return (props) => <Component {...props} params={useParams()} />;
}

class Quiz extends Component {
	constructor(props) {
		super(props);
		this.state = {
			data: new data(),
			quiz_id: this.props.params.quiz,
			loading: true,
		};
	}

	componentDidMount() {
		let getData = {
			getToken: async () => {
				let token = CookieLib.getCookieToken();
				let id = await axios.get(`localhost:8001/token/${token}/id`);
				// let id = "123213121";
				if (!token || !id) {
					token = await axios
						.post("/token/create-respondent")
						.then((x) => x.data)
						.catch(() => {});
					CookieLib.setCookieToken(token);
				}
				this.setState({ token, id });
			},
			checkPermission: async () => {
				let check = await axios
					.get(`localhost:8001/token/${this.state.quiz_id}/check_researcher`)
					.then((x) => x.data);
				// let check = true;
				this.setState({ check });
			},
			getTemplates: async () => {
				let templates = await axios
					.get(`localhost:8001/templates`)
					.then((x) => x.data);
				// let templates = [
				// 	{
				// 		name: "Шаблон 1",
				// 		id: 1,
				// 	},
				// 	{
				// 		name: "Что-то еще",
				// 		id: 2,
				// 	},
				// ];
				this.setState({ templates });
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

	async submit() {
		let data = await axios.post(`/quizes`, {
			name: this.state.name,
			description: this.state.description,
			template_id: this.state.template_id,
		});
		if (data.status === 200) this.props.history.push(`/quizes/${data.data.id}`);
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
					<a id="text">Создание опроса</a>
				</div>

				<div id="quizTile">
					<div id="createQuizTile1" className="row">
						<a id="quizText">Название опроса</a>
						<input
							id="search"
							value={this.state.name}
							onChange={(e) => this.setState({ name: e.target.value })}
							type="text"
							placeholder="Write something.."
						/>
					</div>

					<div id="createQuizTile1" className="row">
						<a id="quizText">Описание</a>
						<textarea
							id="descriptionArea"
							value={this.state.description}
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
						<select id="select" value={this.state.template_id}>
							{this.state.templates.map((x) => (
								<option
									key={x.template_id}
									onChange={() => this.setState({ template_id: x.template_id })}
									value={x.template_id}
								>
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
			<Navigate to="/quizes" replace={true} />
		);
	}
}

export default withParams(Quiz);
