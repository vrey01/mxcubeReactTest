/** @jsx React.DOM */

var DCMethods = React.createClass({
     getDefaultProps: function() {
         this.parameters = "";
         return { disabled: true };
     },
     show_discrete_parameters: function() {
         this.parameters = <DiscreteParameters/>
         this.forceUpdate();
     },
     _add_queue_item: function(item) { 
         if (this.props.disabled) {
           this.props.disabled=item["kind"]!="sample";
           this.forceUpdate();
         }
     },
     componentWillMount: function() {
        window.app_dispatcher.on("queue:new_item", this._add_queue_item);
     },
     componentWillUnMount: function() {
       window.app_dispatcher.off("queue:new_item", this._add_queue_item);
     },
     render: function() {
         var parameters = "";

         return <div>
                  <span className="label label-default">Data collection methods</span>
                  <br></br>
                  <div className="btn-group top5">
                      <button type="button" className="btn btn-default" onClick={this.show_discrete_parameters} disabled={this.props.disabled}>Discrete</button>
                      <button type="button" className="btn btn-default" disabled={this.props.disabled}>Characterisation</button>
                      <button type="button" className="btn btn-default" disabled={this.props.disabled}>Energy scan</button>
                      <div className="btn-group">
                        <button type="button" disabled={this.props.disabled} className="btn btn-default dropdown-toggle" data-toggle="dropdown">
                         Advanced&nbsp; 
                         <span className="caret"></span>
                       </button>
                       <ul className="dropdown-menu" role="menu">
                          <li><a href="#">Mesh</a></li>
                          <li><a href="#">MXPressO</a></li>
                          <li><a href="#">Enhanced characterisation</a></li>
                      </ul>
                    </div>
                 </div>
                 <div className="text-left top7">
                   {this.parameters}
                 </div>
               </div>
    }
});

