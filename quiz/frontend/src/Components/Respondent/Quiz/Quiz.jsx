import React, { Component } from "react";
import data from "../../../data";
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
			data: new data(),
			quiz_id: this.props.params.quiz,
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
						.post("/token/create-respondent")
						.then((x) => x.data)
						.catch(() => {});
					CookieLib.setCookieToken(token);
				}
				this.setState({ token, id });
			},
			checkPermission: async () => {
				let check = await axios
					.get(`/quizes/${this.state.quiz_id}/respondent/${this.state.id}`)
					.then((x) => x.data);
				// let check = true;
				this.setState({ check });
			},
			getQuiz: async () => {
				let quiz = await axios
					.get(`/quizes/${this.state.quiz_id}`, {
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
						.get(`/templates/${quiz.template.id}`)
						.then((x) => x.data),
					results: await axios.get(`/results`, {
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
