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

    return WidgetAdmin;

  }).call(this);

}).call(this);
