import os
import json
from datetime import datetime
from playwright.sync_api import Page

_screenshots_folder = None


def create_screenshot_folder(base_name="test_result"):
    global _screenshots_folder
    if _screenshots_folder is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        _screenshots_folder = os.path.join("reports", f"{base_name}_{timestamp}")
        os.makedirs(_screenshots_folder, exist_ok=True)
    return _screenshots_folder


def login_to_site(
    page: Page,
    url: str,
    username: str,
    password: str,
):
    page.goto(url)
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)
    page.locator("#login-button").click()
    page.wait_for_load_state("load")


def load_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def exclude_keys(data, keys_to_exclude):
    if isinstance(data, dict):
        return {
            key: exclude_keys(value, keys_to_exclude)
            for key, value in data.items()
            if key not in keys_to_exclude
        }
    elif isinstance(data, list):
        return [exclude_keys(item, keys_to_exclude) for item in data]
    else:
        return data


def normalize_strings(data):
    if isinstance(data, dict):
        return {key: normalize_strings(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [normalize_strings(item) for item in data]
    elif isinstance(data, str):
        return data.lower()
    else:
        return data


def prepare_for_comparison(data, keys_to_exclude=None, normalize_case=True):
    if keys_to_exclude:
        data = exclude_keys(data, keys_to_exclude)
    if normalize_case:
        data = normalize_strings(data)
    return data


def get_type_description(value):
    if isinstance(value, dict):
        return "object"
    elif isinstance(value, list):
        return "array"
    elif value is None:
        return "null"
    else:
        return str(type(value).__name__)


def sort_routes_by_route_name(data):
    if isinstance(data, dict):
        if "routes" in data and isinstance(data["routes"], list):
            data["routes"] = sorted(
                data["routes"],
                key=lambda x: x.get("parameters", {}).get("route_name", ""),
            )
        for key, value in data.items():
            data[key] = sort_routes_by_route_name(value)
        return data
    elif isinstance(data, list):
        return [sort_routes_by_route_name(item) for item in data]
    else:
        return data


def get_all_differences(actual, expected, path=""):
    differences = []

    if isinstance(actual, dict) and isinstance(expected, dict):
        all_keys = set(actual.keys()) | set(expected.keys())
        for key in all_keys:
            new_path = f"{path}.{key}" if path else key

            if key not in actual:
                expected_value = expected[key]
                if isinstance(expected_value, (dict, list)):
                    differences.append(
                        {
                            "key": new_path,
                            "expected": get_type_description(expected_value),
                            "actual": "key is not presented",
                            "type": "missing_in_actual",
                        }
                    )
                else:
                    differences.append(
                        {
                            "key": new_path,
                            "expected": expected_value,
                            "actual": "key is not presented",
                            "type": "missing_in_actual",
                        }
                    )
            elif key not in expected:
                actual_value = actual[key]
                if isinstance(actual_value, (dict, list)):
                    differences.append(
                        {
                            "key": new_path,
                            "expected": "key is not presented",
                            "actual": get_type_description(actual_value),
                            "type": "extra_in_actual",
                        }
                    )
                else:
                    differences.append(
                        {
                            "key": new_path,
                            "expected": "key is not presented",
                            "actual": actual_value,
                            "type": "extra_in_actual",
                        }
                    )
            else:
                actual_value = actual[key]
                expected_value = expected[key]

                if isinstance(actual_value, list) and isinstance(expected_value, list):
                    if len(actual_value) != len(expected_value):
                        differences.append(
                            {
                                "key": f"{new_path}[]",
                                "expected": f"{len(expected_value)} elements",
                                "actual": f"{len(actual_value)} elements",
                                "type": "array_length_mismatch",
                            }
                        )
                    else:
                        for i in range(len(actual_value)):
                            diff = get_all_differences(
                                actual_value[i], expected_value[i], f"{new_path}[{i}]"
                            )
                            if diff:
                                differences.extend(diff)
                elif isinstance(actual_value, dict) and isinstance(
                    expected_value, dict
                ):
                    differences.extend(
                        get_all_differences(actual_value, expected_value, new_path)
                    )
                elif actual_value != expected_value:
                    differences.append(
                        {
                            "key": new_path,
                            "expected": expected_value,
                            "actual": actual_value,
                            "type": "value_changed",
                        }
                    )

    elif isinstance(actual, list) and isinstance(expected, list):
        if len(actual) != len(expected):
            differences.append(
                {
                    "key": f"{path}[]",
                    "expected": f"{len(expected)} elements",
                    "actual": f"{len(actual)} elements",
                    "type": "array_length_mismatch",
                }
            )
        else:
            for i in range(len(actual)):
                diff = get_all_differences(actual[i], expected[i], f"{path}[{i}]")
                if diff:
                    differences.extend(diff)

    else:
        if actual != expected:
            differences.append(
                {
                    "key": path,
                    "expected": expected,
                    "actual": actual,
                    "type": "value_changed",
                }
            )

    return differences


def save_diff_report(differences, report_file):
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(differences, f, indent=2, ensure_ascii=False)
