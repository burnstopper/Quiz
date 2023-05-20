import React, { Component } from "react";
import "./Quiz.css";
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
			quiz_id: this.props.params.quiz,
			loading: true,
		};
	}

	async createToken() {
		let token = await axios
			.post("http://localhost:8001/api/token/create_respondent")
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
					.get(`http://localhost:8001/api/token/${token}/id`)
					.then((x) => x.data);
				if (!token) token = await this.createToken();

				this.setState({ token, id });
			},
			checkPermission: async () => {
				let check = await axios
					.get(
						`http://localhost:8001/api/quizes/${this.state.quiz_id}/respondent/${this.state.id}`
					)
					.then((x) => x.data);
				// let check = true;
				this.setState({ check });
			},
			getQuiz: async () => {
				let quiz = await axios
					.get(`http://localhost:8001/api/quizes/${this.state.quiz_id}`, {
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
						.get(`http://localhost:8001/api/templates/${quiz.template.id}`)
						.then((x) => x.data),
					results: await axios.get(`http://localhost:8001/api/results`, {
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
		) : this.state.check && this.state.quiz?.name ? (
			<div className="parent">
				<div id="upTile">
					<p id="text">{this.state.quiz.name}</p>
					<p id="desc">{this.state.quiz.description}</p>
				</div>

				<div id="btnTile">
					{this.state.quiz.template.tests_ids.map((x, i) => {
						console.log(this.state.quiz.results[x]?.length);
						if (
							this.state.quiz.results[this.state.quiz.template.tests_ids[i - 1]]
								?.length > 0 ||
							i === 0
						)
							return (
								<Link
									id="btnQuiz"
									style={{ textDecoration: "none" }}
									to={`${tests[x].link}`}
									key={i}
								>
									<a id="titleTile">{tests[x].name}</a>
									<span class="icon">
										{this.state.quiz.results[x]?.length > 0 ? "✔️" : "⏱️"}
									</span>
								</Link>
							);
						else
							return (
								<div id="btnQuizDis" key={i}>
									<a id="titleTile">{tests[x].name}</a>
									<span class="icon">🔒</span>
								</div>
							);
					})}
				</div>
			</div>
		) : (
			<Navigate to="/quizes" replace={true} />
		);
	}
}

export default withParams(Quiz);
