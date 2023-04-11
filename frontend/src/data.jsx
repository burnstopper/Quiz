const quizes = [
	{
		quiz_id: 1,
		name: "Опрос ВШЭ БКНАД211",
		description:
			'Опрос, созданный для проверки студентов, проходящих курс "Алгоритмы и структуры данных", на выгорание.',
		template_id: 1,
		group_id: 2,
	},
	{
		quiz_id: 1,
		name: "ВЫгорание",
		description:
			'Опрос, созданный для проверки студентов, проходящих курс "Алгоритмы и структуры данных", на выгорание.',
		template_id: 1,
		group_id: 2,
	},
	{
		quiz_id: 1,
		name: "Ух ты",
		description:
			'Опрос, созданный для проверки студентов, проходящих курс "Алгоритмы и структуры данных", на выгорание.',
		template_id: 1,
		group_id: 2,
	},
	{
		quiz_id: 2,
		name: "МГУ опросник",
		description: "Удачных вам голодных игр!",
		template_id: 1,
		group_id: 1,
	},
];

const templates = [
	{
		name: "Стандарт",
		template_id: 1,
	},
	{
		name: "Расширенный",
		template_id: 2,
	},
];

const groups = [
	{
		group_id: 1,
		name: "МГУ ПИ 193",
	},
	{
		group_id: 2,
		name: "ВШЭ БКНАД211",
	},
];

const tests = [
	{
		test_id: 1,
		index: 0,
		template_id: 1,
	},
];

class Dataset {
	constructor(data = { groups, tests, templates, quizes, users: [] }) {
		this.groups = data.groups;
		this.tests = data.tests;
		this.templates = data.templates;
		this.quizes = data.quizes;
		this.users = data.users;
	}

	setUser(user, id) {
		this.users = this.users.filter((x) => x.user_id !== user);
		this.users.push({
			user_id: user,
			group_id: id,
		});
	}
}

export default Dataset;
