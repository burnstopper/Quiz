from app.schemas.template_test import TemplateTestResults as Result


def parse_results_json(results_json: dict) -> list[Result]:
    keys: list[str] = list(results_json.keys())

    results: list[Result | None] = [None] * len(keys)
    for i in range(len(keys)):
        test = {'id': int(keys[i][-1]),
                'results': results_json[keys[i]]
                }

        results[i] = Result(**test)
    return results
