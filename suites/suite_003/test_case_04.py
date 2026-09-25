import json
import os
import requests
from datetime import datetime
from main import (
    load_json_file,
    prepare_for_comparison,
    sort_routes_by_route_name,
    get_all_differences,
    save_diff_report,
    create_screenshot_folder,
)

url = "https://api.routeml.com/api.v4/optimization_problem.php?optimization_problem_id=2A06B6E630B6E21838393266767636D1"
headers = {"X-Api-Key": "BD586208135241879A65BBEDB4B97464"}


def test_user_api():
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Ошибка: {response.status_code}"

    actual = response.json()

    actual_file = "files/actual/get.json"
    os.makedirs(os.path.dirname(actual_file), exist_ok=True)
    with open(actual_file, "w", encoding="utf-8") as f:
        json.dump(actual, f, indent=4, ensure_ascii=False)

    expected = load_json_file("files/expected/001.json")

    exclude = ["q1", "q2", "q3"]
    actual_clean = prepare_for_comparison(actual, exclude, normalize_case=True)
    expected_clean = prepare_for_comparison(expected, exclude, normalize_case=True)

    actual_clean = sort_routes_by_route_name(actual_clean)
    expected_clean = sort_routes_by_route_name(expected_clean)

    differences = get_all_differences(actual_clean, expected_clean)

    if differences:
        report_dir = create_screenshot_folder()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_file = os.path.join(report_dir, f"diff_{timestamp}.json")
        save_diff_report(differences, report_file)
        assert not differences, f"❌ Differences found. Details in: {report_file}"
