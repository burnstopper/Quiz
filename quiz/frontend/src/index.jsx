import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import reportWebVitals from "./reportWebVitals";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Respondent from "./Components/Respondent/List/List";
import Header from "./Components/Menu/Header/Header";
import Quiz from "./Components/Respondent/Quiz/Quiz";
import CreateQuiz from "./Components/Researcher/CreateQuiz/CreateQuiz";
import List from "./Components/Researcher/List/List";
import Templates from "./Components/Researcher/Templates/Template";
import CreateTemplate from "./Components/Researcher/CreateTemplate/CreateTemplate";
import QuizResearch from "./Components/Researcher/Quiz/Quiz";

const root = ReactDOM.createRoot(document.getElementById("root"));
let id = Math.floor(Math.random() * 1000000 + 10000000);
root.render(
	<Router>
		<script src="https://cdn.jsdelivr.net/npm/react/umd/react.production.min.js"></script>

		<script src="https://cdn.jsdelivr.net/npm/react-dom/umd/react-dom.production.min.js"></script>

		<script src="https://cdn.jsdelivr.net/npm/react-bootstrap@next/dist/react-bootstrap.min.js"></script>

		<link rel="preconnect" href="https://fonts.googleapis.com" />
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
		<link
			href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap"
			rel="stylesheet"
		/>

		<Header />
		<div className="main-window">
			<Routes>
				<Route path="/quizes" element={<Respondent id={id} />} />
				<Route path="/quizes/:quiz" element={<Quiz id={id} />} />
				<Route path="/quizes/create" element={<CreateQuiz id={id} />} />
				<Route
					path="/researcher/quizes/:quiz/edit"
					element={<CreateQuiz id={id} />}
				/>
				<Route path="/researcher/quizes" element={<List id={id} />} />
				<Route path="/researcher/templates" element={<Templates id={id} />} />
				<Route
					path="/researcher/templates/:template"
					element={<Templates id={id} />}
				/>
				<Route path="/templates/create" element={<CreateTemplate id={id} />} />
				<Route
					path="/templates/:template"
					element={<CreateTemplate id={id} />}
				/>
				<Route
					path="/researcher/quizes/:quiz"
					element={<QuizResearch id={id} />}
				/>
			</Routes>
		</div>
	</Router>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
