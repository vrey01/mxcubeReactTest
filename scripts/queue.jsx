/** @jsx React.DOM */

var QueueItem = React.createClass({
  render: function() {
       var idref = "#queue_item"+this.props.key;
       var fields = [];
       var fieldno = 0;

       for (field in this.props.fields) {
           var value = this.props.fields[field];
           fields.push( <EditableField key={fieldno} name={field} value={value} /> );
           fieldno += 1;
       }

       return <div className="panel panel-default">
                <div className="panel-heading clearfix">
                  <b className="panel-title pull-left">
                    <a data-toggle="collapse" data-parent="#accordion" href={idref}>
                     {this.props.data.text}
                    </a>
                  </b>
               </div>
               <div id={this.props.key} className="panel-collapse collapse out">
                 <div className="panel-body">
                   {fields}
                 </div>
               </div>
             </div>
     },
});

var Queue = React.createClass({
     getDefaultProps: function() {
       return { "queue_items": [] }
     }, 
     _add_queue_item: function(item) { 
       this.props.queue_items.push(item);
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
           queue_items.push(<QueueItem data={item_text} key={i}/>); 
         }         

         if (queue_items.length>0) execute_queue_button += " btn-primary";

         return <div className="panel panel-default">
                  <div className="panel-heading">Tasks</div>
                  <div className="panel-body">
                    { queue_items }
                    <button type="button" className={execute_queue_button}>Run queue</button>
                  </div>
               </div>
    }
});

