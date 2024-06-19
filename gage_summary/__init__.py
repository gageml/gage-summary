# SPDX-License-Identifier: Apache-2.0

from typing import Any, Literal

import os

__all__ = [
    "Attributes",
    "EchoFormat",
    "Metrics",
    "display_summary",
    "write_summary",
]


Metrics = dict[str, float | int]
Attributes = dict[str, Any]

EchoFormat = Literal["flat", "json", "yaml"]
HeadingLevel = Literal["h1", "h2", "h3", "h4", "h5", "h6"]


def Summary(metrics: dict[str, float | int] | None = None):
    pass


def write_summary(
    *,
    metrics: Metrics,
    attributes: Attributes | None = None,
    filename: str = "summary.json",
    echo: bool = True,
    echo_format: EchoFormat = "flat",
    always_write: bool = False,
):

    summary = _summary(metrics, attributes)
    _maybe_write_summary(always_write, summary, filename)
    if echo:
        _echo_summary(summary, echo_format)


def _summary(metrics: Metrics, attributes: Attributes | None):
    return {
        **({"metrics": metrics} if metrics else {}),
        **({"attributes": attributes} if attributes else {}),
    }


def _maybe_write_summary(always_write: bool, summary: dict[str, Any], filename: str):
    if always_write or _is_cwd_run_dir():
        import json

        with open(filename, "w") as f:
            json.dump(summary, f, indent=2, sort_keys=True)


def _is_cwd_run_dir():
    run_dir = os.getenv("RUN_DIR")
    return run_dir and _compare_paths(run_dir, os.getcwd())


def _compare_paths(p1: str, p2: str):
    return _resolve_path(p1) == _resolve_path(p2)


def _resolve_path(p: str):
    return _realpath(os.path.expanduser(p))


def _realpath(path: str):
    # Workaround for https://bugs.python.org/issue9949
    try:
        link = os.readlink(path)
    except OSError:
        return os.path.realpath(path)
    else:
        path_dir = os.path.dirname(path)
        return os.path.abspath(os.path.join(path_dir, _strip_windows_prefix(link)))


def _strip_windows_prefix(path: str):
    if os.name != "nt":
        return path
    if path.startswith("\\\\?\\"):
        return path[4:]
    return path


def _echo_summary(summary: dict[str, Any], format: EchoFormat):
    if format == "flat":
        _echo_flat(summary)
    elif format == "json":
        _echo_json(summary)
    elif format == "yaml":
        _echo_yaml(summary)
    else:
        raise ValueError(format)


def _echo_flat(summary: dict[str, Any]):
    metrics = summary.get("metrics") or {}
    attributes = summary.get("attributes") or {}
    names = set(list(metrics) + list(attributes))
    missing = object()
    for name in sorted(names):
        metric = metrics.get(name, missing)
        attr = attributes.get(name, missing)
        if metric is not missing and attr is not missing:
            print(f"{name} (metric): {_formatted_metric_value(metric)}")
            print(f"{name} (attribute): {_attribute_value(attr)}")
        elif metric is not missing:
            print(f"{name}: {_formatted_metric_value(metric)}")
        elif attr is not missing:
            print(f"{name}: {_attribute_value(attr)}")
        else:
            assert False, (name, summary)


def _formatted_metric_value(metric: Any):
    value = metric.get("value") if isinstance(metric, dict) else metric
    if isinstance(value, (int, float)):
        return f"{value:g}"
    return str(value) if value is not None else ""


def _attribute_value(attr: Any):
    value = attr.get("value") if isinstance(attr, dict) else attr
    return str(value)


def _echo_json(summary: dict[str, Any]):
    import json

    print(json.dumps(summary, indent=2, sort_keys=True))


def _echo_yaml(summary: dict[str, Any]):
    import yaml

    print(yaml.dump(summary).rstrip())


def display_summary(
    *,
    metrics: Metrics,
    attributes: Attributes | None = None,
    heading_level: HeadingLevel = "h2",
    filename: str = "summary.json",
    always_write: bool = False,
):
    _maybe_write_summary(always_write, _summary(metrics, attributes), filename)
    return _summary_html(metrics, attributes, heading_level)


def _summary_html(metrics: Metrics, attributes: Attributes | None, heading_level: str):
    from IPython.display import HTML

    html = []
    _apply_html_section(metrics, "Metrics", heading_level, html)
    _apply_html_section(attributes, "Attributes", heading_level, html)
    return HTML("\n".join(html))


def _apply_html_section(
    section: Metrics | Attributes | None,
    heading: str,
    heading_level: str,
    html: list[str],
):
    if not section:
        return
    html.append(f"<{heading_level}>{heading}</{heading_level}>")
    html.append("<table>")
    for name, val in section.items():
        val = val.get("value") if isinstance(val, dict) else val
        html.append(f"  <tr><th>{name}</th><td>{val}</td></tr>")
    html.append("</table>")
