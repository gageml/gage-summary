# Display Summary

`display_summary` is used in Jupyter notebooks or other tools
supporting the IPython display API. The function returns an HTML
object that shows the specified summary.

    >>> from gage_summary import display_summary

`display_summary` requires the `IPython` package.

    >>> import IPython

Display some metrics.

    >>> summary = display_summary(
    ...     metrics={
    ...         "loss": 0.123,
    ...         "acc": 0.9543
    ...     }
    ... )

    >>> summary
    <IPython.core.display.HTML object>

    >>> print(summary._repr_html_())  # +diff
    <h2>Metrics</h2>
    <table>
      <tr><th>loss</th><td>0.123</td></tr>
      <tr><th>acc</th><td>0.9543</td></tr>
    </table>

Display metrics and attributes.

    >>> print(display_summary(
    ...     metrics={
    ...         "loss": 0.12345678900112233,
    ...         "acc": 95
    ...     },
    ...     attributes={
    ...         "dtype": "int8"
    ...     }
    ... )._repr_html_())  # +diff
    <h2>Metrics</h2>
    <table>
      <tr><th>loss</th><td>0.12345678900112234</td></tr>
      <tr><th>acc</th><td>95</td></tr>
    </table>
    <h2>Attributes</h2>
    <table>
      <tr><th>dtype</th><td>int8</td></tr>
    </table>

## Writing Summary File

`display_summary` writes a JSON formatted summary file if
`always_write` is true or if there is run in progress. This mirrors
the behavior of `write_summary`.

Use a temp directory.

    >>> cd(make_temp_dir())

The directory is initially empty.

    >>> ls()
    <empty>

Create a sample summary.

    >>> summary = {
    ...   "metrics": {
    ...     "foo": 123,
    ...     "bar": 4.321
    ...   },
    ...   "attributes": {
    ...     "baz": "abc"
    ...   }
    ... }

Call `display_summary` with `always_write` set to true.

    >>> display_summary(**summary, always_write=True)
    <IPython.core.display.HTML object>

    >>> ls()
    summary.json
