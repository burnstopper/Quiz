from app.schemas.template_test import TemplateTestResults


def parse_results_json(results_json: dict) -> list[TemplateTestResults]:
    keys: list[str] = list(results_json.keys())

    results: list[TemplateTestResults | None] = [None] * len(keys)
    for i in range(len(keys)):
        test = {'id': int(keys[i][-1]),
                'results': results_json[keys[i]]
                }

        results[i] = TemplateTestResults(**test)
    return results
