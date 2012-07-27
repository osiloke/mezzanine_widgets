class @WidgetAdmin
  @options_forms: {}


  constructor: ->
#    console.log "Widget Admin Controller"
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
    expose = {color: "#333", loadSpeed: 200, opacity: 0.9}
    $.each($('.widget-add-link'), (i) ->
        link = $(this)
        onBeforeLoad = () ->
        #set the forms slot input to the current widgetslot
          slot_field = $("#widget-form").find("input[name=widgetslot]").get(0)
          slot_name = link.parents(".widget-wrapper").attr("id")
          slot_field.value = slot_name
        overlay = {onBeforeLoad: onBeforeLoad, closeOnEsc: true, expose: expose, closeOnClick: true, close: ':button'}
        link.overlay(overlay)
    )
    $("#edit-widget-form").adminForm({resultParsed: @onEditData})
    $('.widget-edit-link').click((e) =>
        widget_id = e.currentTarget.id.split("-")[1]
        widget_title = e.currentTarget.value
        @onEditForm(e.currentTarget, widget_id, widget_title)
    )
    @

  onEditForm: (link, widget_id, widget_title) ->
    widget = this
    editUrl = "/widget/edit/" + widget_id + "/"
    options = {
      url: editUrl
      success: (data) ->
        expose = {color: "#333", loadSpeed: 200, opacity: 0.9}
        overlay = {load: true, closeOnEsc: true, expose: expose, closeOnClick: true, close: ':button'}
        widget.onEditData(null, data, widget_title)
        $("#edit-widget-form")
          # .adminForm({data: {id: widget_id}})
          .get(0)
          .setAttribute("action", editUrl)

        $(link).overlay(overlay)
        #The load option doesnt seem to be working
        #load overlay after binding to the link
        $(link).overlay(overlay).load()
    }
    $.ajax(options)
    @

  onEditData: (e, params, widget_title) ->
    if params.status == true
      location.reload()
    else
      optHolder = $("#edit-widget-form")
                      .find('fieldset#widget-options')
                      .find(".options")
      switch params.type
         when "ef"
           optHolder.empty()
           optHolder.prepend params.data 
         else
            @
    @

  preSubmit: (e, form) ->
    form.hide()
    $('#editable-loading').show()
    #Accomodate tinymce triggers
    if typeof tinyMCE != "undefined"
      tinyMCE.triggerSave()

  resultParsed: (e, params) ->
      if params.status == true
        location.reload()
      else
        form = params.form
        data = params.data.data
        listSet = form.find('fieldset#widget-list')
        optSet = form.find('fieldset#widget-options')
        optHolder = form.find('fieldset#widget-options').find(".options")
        back = form.find("input[name=back]")
        close = form.find("input[name=close]")
        doer = form.find("input[name=do]")
        action = form.get(0).getAttribute("action")
        resetForm = (form) ->
           listSet = form.find('fieldset#widget-list')
           optSet = form.find('fieldset#widget-options')
           optHolder = form.find('fieldset#widget-options').find(".options")
           form.hide()
           listSet.show()
           optHolder.empty()
           optSet.hide()
           optSet.find("legend").val("Configure this Widget")
           form.get(0).setAttribute("action", action)
           back.hide()
           doer.val("Choose")
        switch params.data.type
           when "fi"
             listSet.hide()
             doer.val("Save")
             optHolder.prepend data
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
           else
             optSet.find("legend").val("You are done! Click save")
             @


      $('#editable-loading').hide()
      form.show()

    doFormSave: (event) ->
      console.log "Form Clicked"