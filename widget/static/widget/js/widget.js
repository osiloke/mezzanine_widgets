(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  this.WidgetAdmin = (function() {

    WidgetAdmin.options_forms = {};

    function WidgetAdmin() {
      this.setupWidgetForms = __bind(this.setupWidgetForms, this);
      this.setupAdmin = __bind(this.setupAdmin, this);
      var not_impl;
      console.log("Widget Admin Controller");
      not_impl = $('a.not-implemented');
      if (not_impl.length > 0) not_impl.each(function(i) {});
      this;
    }

    WidgetAdmin.prototype.setupAdmin = function() {
      var _this = this;
      $(".widget_class select").bind("change", function(e) {
        var type;
        type = $(e.currentTarget).find("option:selected").attr("value");
        if (!(type in _this.options_forms)) {
          return $.getJSON('/widget/options/' + type, function(data) {
            if (data.valid) {
              _this.options_forms[type] = data.opts;
              $("#options-form-holder").html(data.opts);
              return data;
            }
          });
        } else {
          return $("#options-form-holder").html(_this.options_forms[type]);
        }
      });
      return this;
    };

    WidgetAdmin.prototype.setupWidgetForms = function() {
      $("#widget-form").adminForm({
        preSubmit: this.preSubmit,
        resultParsed: this.resultParsed
      });
      $.each($('.widget-add-link'), function(i) {
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
          slot_name = link.parents(".widget-wrapper").attr("id");
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
      return this;
    };

    WidgetAdmin.prototype.getForm = function(e) {
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

    WidgetAdmin.prototype.preSubmit = function(e, form) {
      form.hide();
      $('#editable-loading').show();
      if (typeof tinyMCE !== "undefined") return tinyMCE.triggerSave();
    };

    WidgetAdmin.prototype.editWidget = function(event) {
      return this;
    };

    WidgetAdmin.prototype.resultParsed = function(e, params) {
      var action, back, close, data, doer, form, listSet, optHolder, optSet, resetForm;
      if (params.status === true) {
        location.reload();
      } else {
        form = params.form;
        data = params.data.data;
        listSet = form.find('fieldset#widget-list');
        optSet = form.find('fieldset#widget-options');
        optHolder = form.find('fieldset#widget-options').find(".options");
        back = form.find("input[name=back]");
        close = form.find("input[name=close]");
        doer = form.find("input[name=do]");
        action = form.get(0).getAttribute("action");
        resetForm = function(form) {
          listSet = form.find('fieldset#widget-list');
          optSet = form.find('fieldset#widget-options');
          optHolder = form.find('fieldset#widget-options').find(".options");
          form.hide();
          listSet.show();
          optHolder.empty();
          optSet.hide();
          optSet.find("legend").val("Configure this Widget");
          form.get(0).setAttribute("action", action);
          back.hide();
          return doer.val("Choose");
        };
        switch (params.data.type) {
          case "fi":
            listSet.hide();
            doer.val("Save");
            optHolder.prepend(data);
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
            break;
          default:
            optSet.find("legend").val("You are done! Click save");
            this;
        }
      }
      $('#editable-loading').hide();
      return form.show();
    };

    WidgetAdmin.prototype.doFormSave = function(event) {
      return console.log("Form Clicked");
    };

    return WidgetAdmin;

  })();

}).call(this);
