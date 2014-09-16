/** @jsx React.DOM */

var DCMethods = React.createClass({
     render: function() {
         return <div className="panel panel-default">
                  <div className="panel-heading">Data collection methods</div>
                  <div className="panel-body">
                    <div className="btn-group">
                      <button type="button" className="btn btn-default">Standard</button>
                      <button type="button" className="btn btn-default">Characterisation</button>
                      <button type="button" className="btn btn-default">Helical</button>
                      <button type="button" className="btn btn-default">Energy scan</button>
                      <div className="btn-group">
                        <button type="button" className="btn btn-default dropdown-toggle" data-toggle="dropdown">
                         Advanced 
                         <span className="caret"></span>
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

