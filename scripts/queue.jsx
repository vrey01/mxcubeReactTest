/** @jsx React.DOM */

var Queue = React.createClass({
     getDefaultProps: function() {
       return { "queue_items": [] }
     }, 
     _add_queue_item: function(item) { //_text) {
       if (item["kind"]=="sample") {
         this.props.queue_items.push(item["text"]);
       } else if (item["kind"]=="dc") {
         this.props.queue_items.push(item["text"]);
       }
       this.forceUpdate();
     },
     componentWillMount: function() {
        window.app_dispatcher.on("queue:new_item", this._add_queue_item);
     },
     componentWillUnMount: function() {
       window.app_dispatcher.off("queue:new_item", this._add_queue_item);
     },
     render: function() {
         var queue_items = [];
         var execute_queue_button = "btn btn-block";
         for (i in this.props.queue_items) {
           var item_text = this.props.queue_items[i];
           queue_items.push(<li className="list-group-item">{item_text}</li>);
         }         

         if (queue_items.length>0) execute_queue_button += " btn-primary";

         return <div className="panel panel-default">
                  <div className="panel-heading">Tasks</div>
                  <div className="panel-body">
                    <ul className="list-group">
                      {queue_items}
                    </ul>
                    <button type="button" className={execute_queue_button}>Run queue</button>
                  </div>
               </div>
    }
});

