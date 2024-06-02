# Gage Summary Support

`gage-summary` is a very lightweight utility to support
[Gage](https://github.com/gageml/gage) summaries. It has no install
time dependencies. If it requires a library, the requirement is tested
only as needed (e.g. `display_summary` is specific to Jupyter
notebooks and requires the `IPython` package).

Install the package:

```shell
pip install gage-summary
```

Write Gage summary from a Python script:

```python
from gage_summary import write_summary

write_summary(
  metrics={
    "loss": 0.123,
    "acc": 0.987
  }
)
```

Display summary from a Jupter notebook cell:

```python
from gage_summary import display_summary

display_summary(
  metrics={
    "loss": 0.123,
    "acc": 0.987
  }
)
```

In both cases, the library writes `summary.json` to the current
directory when executed during a Gage run. Otherwise the summary is
just displayed to the user.

Note that Gage summaries are simply JSON formatted metrics and
attributes written to `summary.json` during a run. You're free to
simply write this file yourself without the help of this library. This
library provides aesthetic improvements to summary reporting to users,
either printed to the console or displayed in a Jupyter notebook cell
output.
