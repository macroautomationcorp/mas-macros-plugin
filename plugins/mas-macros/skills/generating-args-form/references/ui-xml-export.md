# `ui.xml` export format

The UIBuilder generates `ui.xml` next to the `.uibproj` on save. It's read by the
host app at runtime to render the script-runner dialog. **Don't generate it yourself
unless the user explicitly asks** — the UIBuilder is the canonical source.

When the user does ask (e.g. "show me what the XML looks like for this", or they're
porting a form to another tool), here's the format.

## Top-level

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="1" type="ScriptRunnerWindow">
  <meta name="My Macro Args" />
  <window id="window_1" title="My Macro Args" width="980" height="640" padding="24" widgetGap="12">
    <script command="" argumentStyle="keyValue" separator="=" />
    <actionBar alignment="right">
      <button id="action_cancel01" text="Cancel" role="cancel" style="secondary" />
      <button id="action_run012345" text="Run" role="run" style="primary" />
    </actionBar>
    <tab id="tab_general0" name="General" order="0">
      <!-- widgets... -->
    </tab>
  </window>
</project>
```

Empty tabs render as self-closing `<tab ... />`.

## Widget elements

Per-kind tag, kebab-case mapped to camelCase:

| Widget kind | XML tag |
| --- | --- |
| text-input | `<textInput>` |
| text-area | `<textArea>` |
| number-input | `<numberInput>` |
| slider | `<slider>` |
| checkbox | `<checkbox>` |
| combobox | `<combobox>` |
| radio-group | `<radioGroup>` |
| file-picker | `<filePicker>` |
| directory-picker | `<directoryPicker>` |
| date-picker | `<datePicker>` |
| time-picker | `<timePicker>` |
| label | `<label>` |
| separator | `<separator>` |
| group-box | `<groupBox>` |

Each widget element has the geometry attributes inline:

```
id="..." name="..."[ parentId="..."] x="24" y="24" width="240" height="36"[ padding="8"]
```

`parentId` and `padding` are emitted only when set.

## Examples per kind

```xml
<textInput id="textinput_a1" name="input_path" x="24" y="24" width="240" height="36" padding="8"
  label="Input path" key="input_path" required="true" placeholder="/path/to/file" defaultValue=""
  helpText="Path to the source file" />

<textArea id="textarea_b2" name="notes" x="24" y="72" width="320" height="80" padding="8"
  label="Notes" key="notes" required="false" rows="4" placeholder="Free-form notes..." defaultValue="" />

<numberInput id="numberinput_c3" name="threads" x="24" y="168" width="160" height="36" padding="8"
  label="Threads" key="threads" required="false" step="1" precision="0" defaultValue="4" min="1" max="64" />

<slider id="slider_d4" name="speed" x="24" y="216" width="280" height="50" padding="8"
  label="Speed" key="speed" required="false" min="0" max="100" step="1" defaultValue="50" showValue="true" suffix="%" />

<checkbox id="checkbox_e5" name="verbose" x="24" y="280" width="200" height="28" padding="4"
  text="Enable verbose logging" key="verbose" required="false" checked="false" />

<combobox id="combobox_f6" name="format" x="24" y="320" width="240" height="36" padding="8"
  label="Output format" key="format" required="true" editable="false" placeholder="Choose..." defaultValue="json">
  <option label="JSON" value="json" />
  <option label="CSV"  value="csv" />
  <option label="YAML" value="yaml" />
</combobox>

<radioGroup id="radio_g7" name="mode" x="24" y="368" width="240" height="80" padding="8"
  label="Mode" key="mode" required="false" direction="vertical" defaultValue="balanced">
  <option label="Fast"     value="fast" />
  <option label="Balanced" value="balanced" />
  <option label="Thorough" value="thorough" />
</radioGroup>

<filePicker id="filepicker_h8" name="config_file" x="24" y="460" width="320" height="36" padding="8"
  label="Config file" key="config_file" required="true" placeholder="Select a file..." defaultValue=""
  filters="*.json;*.yaml;*.yml" />

<directoryPicker id="dirpicker_i9" name="output_dir" x="24" y="508" width="320" height="36" padding="8"
  label="Output directory" key="output_dir" required="true" placeholder="Select a folder..." defaultValue="" />

<datePicker id="datepicker_j10" name="since" x="24" y="556" width="200" height="36" padding="8"
  label="Since" key="since" required="false" format="YYYY-MM-DD" defaultValue="" />

<timePicker id="timepicker_k11" name="deadline" x="240" y="556" width="180" height="36" padding="8"
  label="Deadline" key="deadline" required="false" format="HH:mm" defaultValue="" />

<label id="label_l12" name="label_intro" x="24" y="24" width="320" height="24" text="Connection settings" />

<separator id="sep_m13" name="sep_advanced" x="24" y="60" width="320" height="1" direction="horizontal" label="Advanced" />

<groupBox id="groupbox_n14" name="settings_group" x="24" y="100" width="400" height="200" padding="12"
  title="Output settings" />
```

## Attributes that get omitted

The exporter omits attributes when they equal the default:

- `showLabel` only emitted when `false`
- `labelPosition` only emitted when `"left"`
- `labelGap` only emitted when set
- `helpText` only emitted when non-empty
- `parentId` only when non-null
- `padding` only when set on the widget node
- `min` / `max` / `suffix` for `number-input` / `slider` only when set
- `filters` for `file-picker` only when non-empty
