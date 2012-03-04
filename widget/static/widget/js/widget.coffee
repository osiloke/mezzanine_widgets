class @WidgetAdmin
  @options_forms: {}


  constructor: ->
    console.log "Widget Admin Controller"
    #Catch all actions which are not implemented yet
    not_impl = $('a.not-implemented')
    if not_impl.length > 0
        not_impl.each((i) ->

        )
    @

  setupAdmin: () =>
    $(".widget_class select").bind "change", (e) =>
        type = $(e.currentTarget).find("option:selected").attr("value")
        if not (type of @options_forms)
            $.getJSON('/widget/options/'+type, (data) =>
              if data.valid
                #THere are options for this widget
                #cache options
                @options_forms[type] = data.opts
                $("#options-form-holder").html(data.opts)
                data
            )
        else
          $("#options-form-holder").html(@options_forms[type])
    @

  setupWidgetForms: () =>
    $("#widget-form").adminForm({preSubmit: @preSubmit, resultParsed: @resultParsed})
    $.each($('.widget-add-link'), (i) ->
        link = $(this)
        expose = {color: "#333", loadSpeed: 200, opacity: 0.9}
        onBeforeLoad = () ->
        #set the forms slot input to the current widgetslot
          slot_field = $("#widget-form").find("input[name=widgetslot]").get(0)
          slot_name = link.parents(".widget-wrapper").attr("id")
          slot_field.value = slot_name
        overlay = {onBeforeLoad: onBeforeLoad, closeOnEsc: true, expose: expose, closeOnClick: true, close: ':button'}
        link.overlay(overlay)
    )
    @

  getForm: (e) ->
    expose = {color: "#333", loadSpeed: 200, opacity: 0.9}
    overlay = {closeOnEsc: true, expose: expose, closeOnClick: true, close: ':button'}
    widget_id = $(this).attr("id").split("-")[1]
    options = {
    url: "/widget/edit/" + widget_id
    success: (data) ->
      $("#edit-widget-form")
      .adminForm({preSubmit: @preSubmit, resultParsed: @resultParsed})
      .overlay(overlay)
    }
    $.ajax(options)
    @

  preSubmit: (e, form) ->
    form.hide()
    $('#editable-loading').show()
    if typeof tinyMCE != "undefined"
      tinyMCE.triggerSave()

  editWidget: (event) ->
    @

  resultParsed: (e, params) ->
    if params.status == true
      location.reload()
    else
      form = params.form
      data = params.data.data
      back = form.find("input[name=back]")
      close = form.find("input[name=close]")
      action = form.get(0).getAttribute("action")
      resetForm = (form) ->
        listSet = form.find('#id_widget_class').parent()
        form.hide()
        listSet.show()
        optSet.empty().hide()
        form.get(0).setAttribute("action", action)
        back.hide()

      switch params.data.type
        when "fi"
          listSet = form.find('#id_widget_class').parent()
          optSet = form.find('fieldset#widget-options')
          listSet.hide()
          optSet.prepend data
          optSet.show()
          form.get(0).setAttribute("action", "/widget/create/")
          back.show()

          back.bind('click', (event) ->
              event.preventDefault()
              resetForm(form)
              form.show()
          )

          close.bind('click', (event) ->
              resetForm(form)
          )
        when "nf"
          @


    $('#editable-loading').hide()
    form.show()

  doFormSave: (event) ->
    console.log "Form Clicked"