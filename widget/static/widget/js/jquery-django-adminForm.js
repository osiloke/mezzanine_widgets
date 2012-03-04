(function(jQuery) {
    function inputs(form)   {
        return form.find(":input:visible:not(:button)");
    }

    $.widget("easyadmin.adminForm",
        {
        options: {
            preSubmit:null,
            postSuccess:null,
            type: 'p',
            callback: false,
            fields: false,
            dom: this,
            event: 'submit',
            submitHandler: null
        },
        _settings: null,
        _status:false,
        _form:null,
        _create: function(event) {
            this._form = $("form#"+this.element[0].id);
            this._settings = this.options;
            _.bindAll(this);
            this._form.bind("submit",this._submitForm);
        },
        _submitForm: function(event){

            event.preventDefault();
            var widget = this; 
            var data = this._form.serialize();
            widget._trigger("preSubmit",'',widget._form);
            this._form.ajaxSubmit({
                url:widget._form.attr('action'),
//                data:data,
                type:'post',
                datatype:'json',
                traditional: true,
                error: function()   {
                    widget._status = false;
                },
                success: function(data, textStatus, xhr) {
                    widget._status = data.valid;
                    var return_type = data.type;
                    if (!widget._status && typeof data.errors !== 'undefined' )    {
                        var get_form_error_position = function(key) {
                            key = key || '__all__';
                            if (key == '__all__') {
                                var filter = ':first';
                            } else {
                                var filter = ':first[id^=id_' + key.replace('__all__', '') + ']';
                            }
                            return inputs(widget._form).filter(filter).parent();
                        };
                        if (widget._settings.type == 'p')    {

                            widget._form.find('ul.errorlist').remove();
                            $.each(data.errors, function(key, val)  {
                                if (key.indexOf('__all__') >= 0)   {

                                    var error = get_form_error_position(key);
                                    if (error.prev().is('ul.errorlist')) {
                                        error.prev().before('<ul class="errorlist"><li>' + val + '</li></ul>');
                                    }
                                    else    {
                                        error.before('<ul class="errorlist"><li>' + val + '</li></ul>');
                                    }
                                }
                                else    {

                                    widget._form.find('#' + key+':first').parent().before('<ul class="errorlist"><li>' + val + '</li></ul>');
                                }
                            });
                        }
                        if (widget._settings.type == 'table')   {
                            inputs(widget._form).prev('ul.errorlist').remove();
                            widget._form.find('tr:has(ul.errorlist)').remove();
                            $.each(data.errors, function(key, val)  {
                                if (key.indexOf('__all__') >= 0)   {
                                    get_form_error_position(key).parent().before('<tr><td colspan="2"><ul class="errorlist"><li>' + val + '.</li></ul></td></tr>');
                                }
                                else    {
                                    $('#' + key).before('<ul class="errorlist"><li>' + val + '</li></ul>');
                                }
                            });
                        }
                        if (widget._settings.type == 'ul')  {
                            inputs(widget._form).prev().prev('ul.errorlist').remove();
                            widget._form.find('li:has(ul.errorlist)').remove();
                            $.each(data.errors, function(key, val)  {
                                if (key.indexOf('__all__') >= 0)   {
                                    get_form_error_position(key).before('<li><ul class="errorlist"><li>' + val + '</li></ul></li>');
                                }
                                else    {
                                    $('#' + key).prev().before('<ul class="errorlist"><li>' + val + '</li></ul>');
                                }
                            });
                        }
                    }
                    widget._trigger('resultParsed','',{data:data, form:widget._form, status:widget._status});
                }
            });
            return false;
        },
        /**
         *
         * @param key
         * @param value
         */
        _setOption: function( key, value ) {
            var oldValue = this.options[key];
            this.options[ key ] = value;
            this._trigger("setOption", { type: "setOption" }, {
                option: key,
                original: oldValue,
                current: value
              });
            this._update();
            $.Widget.prototype._setOption.apply(this,arguments)

           },
            _update: function() {
            },
       destroy: function() {
        $.Widget.prototype.destroy.call(this);
       }
     });
})(jQuery);