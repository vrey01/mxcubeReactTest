/** @jsx React.DOM */

var DCMethods = React.createClass({
     getDefaultProps: function() {
         return { disabled: true };
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
     add_discrete: function() {
       window.app_dispatcher.trigger("queue:new_item", { kind: "dc", "text": "discrete" });
     },
     add_characterisation: function() {
     },
     add_egyscan: function() {
     },
     render: function() {
         return <div className="panel panel-default">
                  <div className="panel-heading">
                    <h4 className="panel-title">Data collection methods</h4>
                  </div>
                  <div className="panel-body">
                    <div className="btn-group">
                      <button type="button" className="btn btn-default" onClick={this.add_discrete} disabled={this.props.disabled}>
                        <span className="glyphicon glyphicon-plus"></span> Discrete
                      </button>
                      <button type="button" className="btn btn-default" onClick={this.add_characterisation} disabled={this.props.disabled}>
                        <span className="glyphicon glyphicon-plus"></span> Characterisation 
                      </button>
                      <button type="button" className="btn btn-default" onClick={this.add_egyscan} disabled={this.props.disabled}>
                        <span className="glyphicon glyphicon-plus"></span> Energy scan
                      </button>
                      <div className="btn-group">
                        <button type="button" disabled={this.props.disabled} className="btn btn-default dropdown-toggle" data-toggle="dropdown">
                         <span className="glyphicon glyphicon-plus"></span> Advanced <span className="caret"></span>
                       </button>
                       <ul className="dropdown-menu" role="menu">
                          <li><a href="#">Mesh</a></li>
                          <li><a href="#">MXPressO</a></li>
                          <li><a href="#">Enhanced characterisation</a></li>
                      </ul>
                    </div>
                   </div>
                 </div>
               </div>
    }
});

