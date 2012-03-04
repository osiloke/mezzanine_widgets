(function() {

  this.WidgetAdmin = (function() {

    WidgetAdmin.options_forms = {};

    function WidgetAdmin() {
      this;
    }

    WidgetAdmin.setupAdmin = function() {
      $(".widget_class select").bind("change", function(e) {
        var type;
        type = $(e.currentTarget).find("option:selected").attr("value");
        if (!(type in WidgetAdmin.options_forms)) {
          return $.getJSON('/widget/options/' + type, function(data) {
            if (data.valid) {
              WidgetAdmin.options_forms[type] = data.opts;
              $("#options-form-holder").html(data.opts);
              return data;
            }
          });
        } else {
          return $("#options-form-holder").html(WidgetAdmin.options_forms[type]);
        }
      });
      return WidgetAdmin;
    };

    WidgetAdmin.setupWidgetForms = function() {
      $("#widget-form").adminForm({
        preSubmit: WidgetAdmin.preSubmit,
        resultParsed: WidgetAdmin.resultParsed
      });
      return $.each($('.widget-form-link'), function(i) {
        var expose, link, onBeforeLoad, overlay;
        link = $(this);
        expose = {
          color: "#333",
          loadSpeed: 200,
          opacity: 0.9
        };
        onBeforeLoad = function() {
          var slot_field, slot_name;
          slot_field = $("#widget-form").find("input[name=widgetslot]").get(0);
          slot_name = link.parent(".widget_wrapper").attr("id");
          return slot_field.value = slot_name;
        };
        overlay = {
          onBeforeLoad: onBeforeLoad,
          closeOnEsc: true,
          expose: expose,
          closeOnClick: true,
          close: ':button'
        };
        return link.overlay(overlay);
      });
    };

    WidgetAdmin.getForm = function(e) {
      var expose, options, overlay, widget_id;
      expose = {
        color: "#333",
        loadSpeed: 200,
        opacity: 0.9
      };
      overlay = {
        closeOnEsc: true,
        expose: expose,
        closeOnClick: true,
        close: ':button'
      };
      widget_id = $(this).attr("id").split("-")[1];
      options = {
        url: "/widget/edit/" + widget_id,
        success: function(data) {
          return $("#edit-widget-form").adminForm({
            preSubmit: this.preSubmit,
            resultParsed: this.resultParsed
          }).overlay(overlay);
        }
      };
      $.ajax(options);
      return this;
    };

    WidgetAdmin.preSubmit = function(e, form) {
      form.hide();
      $('#editable-loading').show();
      if (typeof tinyMCE !== "undefined") return tinyMCE.triggerSave();
    };

    WidgetAdmin.editWidget = function(event) {
      return this;
    };

    WidgetAdmin.resultParsed = function(e, params) {
      var action, back, close, data, form, listSet, optSet, resetForm;
      if (params.status === true) {
        location.reload();
      } else {
        form = params.form;
        data = params.data.data;
        back = form.find("input[name=back]");
        close = form.find("input[name=close]");
        action = form.get(0).getAttribute("action");
        resetForm = function(form) {
          var listSet;
          listSet = form.find('#id_widget_class').parent();
          form.hide();
          listSet.show();
          optSet.empty().hide();
          form.get(0).setAttribute("action", action);
          return back.hide();
        };
        switch (params.data.type) {
          case "fi":
            listSet = form.find('#id_widget_class').parent();
            optSet = form.find('fieldset#widget-options');
            listSet.hide();
            optSet.prepend(data);
            optSet.show();
            form.get(0).setAttribute("action", "/widget/create/");
            back.show();
            back.bind('click', function(event) {
              event.preventDefault();
              resetForm(form);
              return form.show();
            });
            close.bind('click', function(event) {
              return resetForm(form);
            });
            break;
          case "nf":
            this;
        }
      }
      $('#editable-loading').hide();
      return form.show();
    };

    WidgetAdmin.doFormSave = function(event) {
      return console.log("Form Clicked");
    };

    return WidgetAdmin;

  }).call(this);

}).call(this);
