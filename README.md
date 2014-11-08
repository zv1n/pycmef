# Javascript API

## cmef.ready(function)

The `cmef.ready` method should be used to configure all experiment environment.  It will be called after all CMEF and Python components have initialized.

```Javascript
cmef.ready(function() {
  $('#next').click(function(event){
    cmef.emit('next', {});
  });
});
```

The above example will emit a 'next' signal when element with id of `next` is pressed.  Available signals are discussed in the [Signals](#signals) section.

## cmef.input_selectors(Array)

Use the `input_selectors` method to select what input values should be collected for storage in the experiment output file.

```Javascript
  cmef.input_selectors([
  'input[name=Gender]:checked',
  'input[name=Race]:checked',
  'input[name=Age]'
  ]);
```

## cmef.collect_response()

The `collect_response` method will collect all inputs specified by `input_selectors`.

## Internals

All internal Python signals and slots can be accessed via the `window._experiment` bridge property.

Currently, exposed bridge elements are:

|Name|Description|
|---|---
|experiment|The entire experiment configuration file.
|data|The entire permuted experiment data set.
|subsection|The *current subsection*.
|current|The *current* dataset.  This may be a permutation of items listed in `experiment.data`

## Signals

Signals can be sent by a call to the `cmef.emit` method.  This method will trigger an internal Python method associated with the named event.  A Javascript object can be passed in as an argument.  The object will be serialized into JSON for processing in Python.  Once complete, if provided, a callback will be executed.

### Events

Default available events can be seen below:

|Event|Required Inputs|Description
|---|---|---
|start||(Internal) Used to start experiment by the CMEF Selftest.
|next||Move to the next subsection/section. (Note: JS callback may not be executed.)
|refresh||Refresh the current page (and user input will be lost).
|show||(Internal) Used by CMEF (cmef.coffee) to signal when the required libraries are loaded.

### Callbacks

The callback methods passed into an `emit` call can take 1 argument, which is the `response` from the Python signal handler.  The response from the Python signal handler will automatically convert the parameter into a JS Object, Array, or String.  Each signal is required to maintain a consistent response type.

### Example

```Javascript
  $('#next').click(function(event){
    cmef.emit('next', {}, function(response) {
      console.log(response);
    });
  });
```

The above method will tricker the `next` signal on button click.  The response callback provided will then print the response to the console.  Depending on the speed of loading, this callback may not complete or run at all.

# Auto Handlers

The handlers listed below will be automatically handled by the CMEF framework on page load.  The framework relies on [Handlebars.js](http://handlebarsjs.com/) for the templating.  The contents of the template consist only of the `current` data, as listed in the [Javascript API](#javascript-api) section.

## data-enable-on

```HTML
<input type="button" id="next" value="Continue" class="pure-button"

  data-enable-on="[name='answer']"

>
```

Set the `data-enable-on` to a JQuery selector to trigger an automatic enable once the selector is changed.  This is primarily for radio buttons, since once selected they cannot be unselected.

## data-default

```HTML
<input type="button" id="next" value="Continue" class="pure-button"

  data-default="true"

>
```

Set `data-default` to `true` if you wish for the button to follow a standard operation.  The ID of the object must match an ID in the list below.

|ID|Operation
|---|---
|next|Move to the next subsection or section.
|refresh|Trigger a page refresh. (FUTURE)
|back|Navigate back to the previous subsection. (FUTURE)

## data-attribute & data-value

```HTML
<img

  data-attribute="src"
  data-value="{{data.image}}"

/>
```

Set the `data-attribute` to the data attribute you want set.  Set the `data-value` to the Handlebars-compliant value you want the attribute set to.  In the above image, the `src` attribute is populated with the `data.image` value of the `current` dataset.

## data-content & data-value

```HTML
<span

  data-content
  data-value="{{data.question.text}}"

></span>
```

Add `data-content` and add a `data-value` containg the Handlebars-compliant value to the HTML element.  The `innerHTML` of the element will be replaced by the content of the Handlebars element.

