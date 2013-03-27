class @WidgetAdmin
  @options_forms: {}
  widget_status_icon_toggle: {
    2: {"ico":"icon-thumbs-up", "message": "Published", "prefix": "Unpublish"},
    1: {"ico":"icon-thumbs-down", "messsage": "Unpublished", "prefix":"Publish"}
  }

  constructor: ->
#    console.log "Widget Admin Controller"
    #Catch all actions which are not implemented yet
    not_impl = $('a.not-implemented')
    if not_impl.length > 0
        not_impl.each((i) ->

        )
    #some neccessary jq config
    # $(".widget-edit-link, .widget-delete-link").tooltip {placement:"right"}
    @setupAdmin()
    @setupWidgetForms()
    @setupSortableWidgets()
    @setupWidgetStatusHandler()
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

    #Setup Edit Form for ajax post submission
    $("#edit-widget-form").adminForm({resultParsed: @onEditData})

    #Setup Edit Form Triggers
    $('.widget-edit-link').click((e) =>
        widget_id = e.currentTarget.id.split("-")[1]
        widget_title = e.currentTarget.parentElement.parentElement.parentElement.id
        @onEditForm(e.currentTarget, widget_id, widget_title)
        $('#editForm').modal()
        e.preventDefault();
    )
    @

  setupWidgetStatusHandler: =>
    status_icons = @widget_status_icon_toggle
    $(".widget-publish-link").tooltip {
      placement:"right",
      title: () ->
        widget_status = @.id.split("-")[-1..][0]
        return status_icons[widget_status]["prefix"]
    }
    $(".widget-publish-link").click((e) =>
      id_split = e.currentTarget.id.split("-")
      widget_id = id_split[1]
      widget_title = $(e.currentTarget).attr('data-original-title')
      callback = (data) =>
        if data.status == true
#          icon = $("#" + e.currentTarget.id + " i")
          icon = e.currentTarget.getElementsByTagName("i")[0]
          toggle = @widget_status_icon_toggle[data.published]
          new_class = toggle["ico"]
          icon.className = new_class
          old_id = e.currentTarget.id
          new_id = old_id[...-1] + data.published
          e.currentTarget.id = new_id


      @remoteCall(e.currentTarget, window.__widget_status_url, {"id":widget_id}, callback)
      e.preventDefault()
    )

  setupSortableWidgets: ->
    # AJAX callback that's triggered when dragging a widget to re-order
    # Based on mezzanine
    updateOrdering = (event, ui) ->
#      $uiItem = $(ui.item)
#      if $uiItem.parent().is('.widget-sortable') then $uiItem.remove()

      next = ui.item.next()
      next.css({'-moz-transition':'none', '-webkit-transition':'none', 'transition':'none'})
      setTimeout(next.css.bind(next, {'-moz-transition':'border-top-width 0.1s ease-in', '-webkit-transition':'border-top-width 0.1s ease-in', 'transition':'border-top-width 0.1s ease-in'}))

      args =
        'ordering_from': $(this).sortable('toArray').toString(),
        'ordering_to': $(ui.item).parent().sortable('toArray').toString(),
#      console.log $(this), $(ui.item)
      if args['ordering_from'] != args['ordering_to']
        # Branch changed - set the new parent ID.
        args['moved_widget'] = $(ui.item).attr('id')
        args['moved_parent'] = $(ui.item).parent().parent().attr('id')
        if args['moved_parent'] == 'widget-sortable'
          delete args['moved_parent']
      else
        delete args['ordering_to']
        delete args['widget_class_to']

      $.post(window.__widget_ordering_url, args, (data) ->
        if not data
          alert("Error occured: " + data + "\nWidget ordering wasn't updated.");

      ) 
    stylesheet = $('style[name=impostor_size]')[0].sheet
    `rule = stylesheet.rules ? stylesheet.rules[0].style : stylesheet.cssRules[0].style`
    setPadding = (atHeight) ->
        rule.cssText = 'border-top-width: '+atHeight+'px'

    $('.widget-sortable').sortable({
      handle: '.ordering',
      opacity: '.7',
      stop: updateOrdering,
      forcePlaceholderSize: true,
      dropOnEmpty: true,
      placeholder: 'placeholder',
      helper: 'clone',
      revert: 150,

#      start: (ev, ui) ->
#        setPadding(ui.item.height())
    })
      .sortable('option', 'connectWith', '.widget-sortable')
      .bind('sortstart', (event, ui) ->
          setPadding(ui.item.height())
#          $uiItem = $(ui.item)
#          $uiItem.clone().show().insertBefore($uiItem)
      )
      .disableSelection()

  #edit form handler
  onEditForm: (link, widget_id, widget_title) ->
    widget = this
    url = "/widget/edit/" + widget_id + "/"
    options = {
      url: url
      success: (data) ->
        widget.onEditData(null, data, widget_title)
        $("#edit-widget-form")
          .get(0)
          .setAttribute("action", url)
    }
    $.ajax(options)
    @

  remoteCall: (e, url, params, callback) ->
    widget = this
    options = {
      type: "POST"
      url: url
      data: params
      success: (data) ->
        callback(data)

    }
    if callback
      options["success"] = (data) ->
        callback(data)

    $.ajax(options)
    @

  #edit form result handler
  onEditData: (e, params, widget_title) ->
    if params.status == true
      location.reload()
    else
      optHolder = $("#edit-widget-form")
                      .find('fieldset#widget-options')
                      .find(".options")

      #set modal title
      $("#editForm h3#title").text("Edit " + widget_title)
      switch params.type
         when "ef"
           optHolder.empty()
           optHolder.prepend params.data

           if params.extra_js
             for js in params.extra_js
              eval(js)
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
           $("#editForm h3#title").text("Configure this Widget")
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
             $("#editForm h3#title").text("You are done! Click save")
             @


      $('#editable-loading').hide()
      form.show()

    #The following functions are used to execute special js init for some widget option types

    wysihtml: (id) ->
      $("#" + id).wysihtml5({"font-styles": true, "emphasis": true, "lists": true, "html": true})

    gloweditor: (id) ->
      editor = new glow.widgets.Editor("#" + id, {theme: "dark"})

    doFormSave: (event) ->
      console.log "Form Clicked"