/** @jsx React.DOM */

var SampleList = React.createClass({
     render: function() {
        id = 0;
        var samples = this.props.samples.map( function(sample) {
             id += 1;
             return <Sample sample={sample} key={id} />;
         }.bind(this));
        return <div className="panel-group">{samples}</div>
     },
});

var Sample = React.createClass({
     
     render: function() {

       var idref = "#"+this.props.key;

       var fields = [];

       fieldno = 0;
       hiddenfields = ['sampleId', 'sampleName'];

       for (field in this.props.sample) { 
           if (hiddenfields.indexOf(field) >= 0){
                continue;
           }
           var value = this.props.sample[field];
           fields.push( <EditableField key={fieldno} sampleid={this.props.sample.sampleId} name={field} value={value} /> );
           fieldno += 1;
       }

       return <div className="panel panel-default">
    <div className="panel-heading">
      <h4 className="panel-title">
        <a data-toggle="collapse" data-parent="#accordion" href={idref}>
          {this.props.sample.sampleName}
        </a>
      </h4>
    </div>
    <div id={this.props.key} className="panel-collapse collapse out">
      <div className="panel-body">
            {fields}
      </div>
    </div>
  </div>
     },

});

var EditableField = React.createClass({

   componentDidMount: function() {
    $(this.refs.editable.getDOMNode()).editable();
   }, 

   render: function() {
       return <p>{this.props.name}: <a href="#" ref="editable" data-name={this.props.name} data-pk={this.props.sampleid} data-url="/sample_field_update" data-type="text" data-title="Edit value">{this.props.value}</a></p>
   } 
})
