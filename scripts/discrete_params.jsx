/** @jsx React.DOM */

var DiscreteParameters = React.createClass({
     _add_button_clicked: function() {
       var params = { "text": "Discrete (" };
       $(this.refs.discrete_dc_form.getDOMNode()).serializeArray().map(function(item) {
         params[item.name] = item.value;
         params["text"]+=item.name+"="+item.value+",";
       }); 
       params["kind"]="dc";
       params["text"] += ")";
       window.app_dispatcher.trigger("queue:new_item", params);
     },
     render: function() {
            return <form className="well form-inline clearfix" role="form" ref="discrete_dc_form">
	               <div className="form-group form-group-sm">
                           <label className="control-label">Oscillation range&nbsp;</label>
                           <input type="text" name="osc_range" className="form-control" placeholder="0.1"></input>
                       </div>&nbsp;
                       <div className="form-group form-group-sm top5">
                          <label className="control-label">Oscillation start&nbsp;</label>
                          <input type="text" name="osc_start" className="form-control" placeholder="0"></input>
                       </div>&nbsp;
                       <div className="form-group form-group-sm top5">
                          <label className="control-label">Exposure time&nbsp;</label>
                          <input type="number" name="exptime" className="form-control" placeholder="0.02" step="0.01"></input>
                       </div>&nbsp;
                       <div className="form-group form-group-sm top5">
                          <label className="control-label">Number of images&nbsp;</label>
                          <input type="number" name="num_images" className="form-control" placeholder="1"></input>
                       </div>  
                       <br></br>
                       <button type="button" className="pull-right btn btn-sm btn-primary" onClick={this._add_button_clicked}>Add</button>
                  </form>
    }
});

