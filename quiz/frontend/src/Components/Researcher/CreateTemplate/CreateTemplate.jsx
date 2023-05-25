import React, { Component } from "react";
import "./CreateTemplate.css";
import CookieLib from "../../../cookielib/index";
import LoadingScreen from "react-loading-screen";
import { Spinner } from "react-bootstrap";
import { Link, Navigate, useParams } from "react-router-dom";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import { Draggable, Droppable } from "react-drag-and-drop";
import Dropdown from "react-bootstrap/Dropdown";
import axios from "axios";
let i = 0;
function isBlank(str) {
	return !str || /^\s*$/.test(str);
}

function withParams(Component) {
	return (props) => <Component {...props} params={useParams()} />;
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
				loading: true,
				template_id: this.props.params?.template,
				isModalOpen: false,
				title: "Опросы",
				list: ["Пусто"],
				name: "",
				template: {
					name: "",
					tests: [],
					quizzes: [],
				},
				edit: false,
				// name: '',
			};
		}

		handleMenu(data, index) {
			let template = this.state.template;
			let element = this.state.tests.filter(
				(x) => !template.tests.find((y) => y.id === x.id)
			)[index];
			template.tests.push(element);

			this.setState({ template });
		}

		handleDrop(data, index) {
			let array = Array.from(this.state.template.tests);
			// let tmp = array[data.tests];
			let result = array_move(array, data.tests, index);
			// array[data.tests] = array[this.index];
			// array[this.index] = tmp;
			let template = this.state.template;
			template.tests = result;
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

		async delete(index) {
			let array = Array.from(this.state.template.tests);
			array.splice(index, 1);
			// let tmp = array[data.tests];
			// array[data.tests] = array[this.index];
			// array[this.index] = tmp;
			let template = this.state.template;
			template.tests = array;
			this.setState({ template });
		}

		async getTemplateData() {
			let template = await axios
				.get(`/api/templates/${this.state.template_id}`)
				.then((x) => x.data)
				.catch((e) => alert(e.response.statusText));

			if (template)
				this.setState({
					name: template.name,
					template,
					edit: true,
				});
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
				// checkPermission: async () => {
				// 	let check = await axios
				// 		.get(
				// 			`/api/token/${this.state.quiz_id}/check_researcher`
				// 		)
				// 		.then((x) => x.data).catch((e) => alert(e.response.statusText));
				// 	// let check = true;
				// 	this.setState({ check });
				// },
				getAllQuizes: async () => {
					let tests = await axios
						.get(`/api/tests`)
						.then((x) => x.data)
						.catch((e) => alert(e.response.statusText));
					// let tests = [
					// 	{ id: 1, name: "Что-то первое" },
					// 	{ id: 2, name: "Что-то второе" },
					// 	{ id: 3, name: "Что-то третье" },
					// 	{ id: 4, name: "Что-то четвертое" },
					// 	{ id: 5, name: "Что-то пятое" },
					// ];
					this.setState({
						tests,
					});
				},
			};
			async function start() {
				for (let i of Object.keys(getData)) {
					await getData[i]();
				}

				if (this.state.template_id && this.state.template_id !== "create")
					await this.getTemplateData();

				this.setState({ loading: false });
			}
			start.bind(this)();
		}

		async submit() {
			if (!this.state.name || this.state.name === "")
				return alert("Вы не ввели название");

			if (this.state.template?.tests?.length <= 0)
				return alert("Список тестов не может быть пустым");
			let data;
			if (!this.state.edit)
				data = await axios
					.post(`/api/templates`, {
						tests_ids: this.state.template.tests.map((x) => x.id),
						name: this.state.name,
					})
					.catch((e) => alert(e.response.statusText));
			else
				data = await axios
					.post(`/api/templates`, {
						id: this.state.template_id,
						tests_ids: this.state.template.tests.map((x) => x.id),
						name: this.state.name,
					})
					.catch((e) => alert(e.response.statusText));
			if (data.status === 200) window.location.href = `/researcher/templates`;
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
						<p id="text">
							{this.state.edit ? "Редактирование" : "Создание"} шаблона
						</p>
						{/* <div className="component-menu">
						<Dropdown>
							<Dropdown.Toggle variant="success" id="dropdown-basic1">
								Добавить тест
							</Dropdown.Toggle>

							<Dropdown.Menu>
								{this.state.tests
									.filter(
										(x) => !this.state.template.tests.find((y) => y.id === x.id)
									)
									.map((x, i) => (
										<Dropdown.Item
											key={i}
											onClick={(data) => this.handleMenu.bind(this)(data, i)}
										>
											<a id="titleTile">{x.name}</a>
										</Dropdown.Item>
									))}
							</Dropdown.Menu>
						</Dropdown>
					</div> */}
					</div>
					{/* <div id="btnTile">
					{this.state.template.tests.map((x, i) => (
						<Droppable
							id="btnQuizes"
							// styles={{ maxWidth: "1200px", minWidth: "900px", width: "80%" }}
							key={i}
							types={["tests"]}
							onDrop={(data) => this.handleDrop.bind(this)(data, i)}
						>
							<Draggable id="draggable" type="tests" data={i}>
								<a id="titleTile">{x.name}</a>
							</Draggable>
						</Droppable>
					))}
				</div> */}
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
						<Dropdown>
							<Dropdown.Toggle variant="success" id="dropdown-basic1">
								Добавить тест
							</Dropdown.Toggle>

							<Dropdown.Menu>
								{this.state.tests
									.filter(
										(x) => !this.state.template.tests.find((y) => y.id === x.id)
									)
									.map((x, i) => (
										<Dropdown.Item
											key={i}
											onClick={(data) => this.handleMenu.bind(this)(data, i)}
										>
											<a id="titleTile">{x.name}</a>
										</Dropdown.Item>
									))}
							</Dropdown.Menu>
						</Dropdown>
					</div>
					<div id="btnTile">
						{this.state.template.tests.map((x, i) => (
							<Droppable
								id="btnQuizes"
								// styles={{ maxWidth: "1200px", minWidth: "900px", width: "80%" }}
								key={i}
								types={["tests"]}
								onDrop={(data) => this.handleDrop.bind(this)(data, i)}
							>
								<Draggable id="draggable" type="tests" data={i}>
									<a onClick={() => this.delete(i)} id="titleDelete">
										❌
									</a>
									<a id="titleTile">{x.name}</a>
								</Draggable>
							</Droppable>
						))}
					</div>
					<div id="downTiles">
						<button id="btnPlayss" onClick={this.submit.bind(this)}>
							Создать
						</button>
					</div>
				</div>
			) : (
				<Navigate to="/quizzes" replace={true} />
			);
		}
	}
);
