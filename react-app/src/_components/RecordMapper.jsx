import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

const defaultProps = {};

class RecordMapper extends Component {
    constructor(props) {
        super(props);
    }

    componentDidMount(){
        var context = this;
        var $ = go.GraphObject.make;  // for conciseness in defining templates
        var myDiagram =
            $(go.Diagram, "mapper-diagram",
                {
                    initialContentAlignment: go.Spot.Center,
                    validCycle: go.Diagram.CycleNotDirected,  // don't allow loops
                    // For this sample, automatically show the state of the diagram's model on the page
                    "ModelChanged": function(e) {
                        if (e.isTransactionFinished) {
                            context.props.onChange(myDiagram.model);
                        }
                    },
                    "undoManager.isEnabled": true
                });
        // myDiagram.toolManager.mouseDownTools.add(new RowResizingTool());
        // myDiagram.toolManager.mouseDownTools.add(new ColumnResizingTool());
        // This template is a Panel that is used to represent each item in a Panel.itemArray.
        // The Panel is data bound to the item object.
        var fieldTemplate =
        $(go.Panel, "TableRow",  // this Panel is a row in the containing Table
            new go.Binding("portId", "name"),  // this Panel is a "port"
            {
                background: "transparent",  // so this port's background can be picked by the mouse
                fromSpot: go.Spot.Right,  // links only go from the right side to the left side
                toSpot: go.Spot.Left,
                // allow drawing links from or to this port:
                fromLinkable: true, toLinkable: true
            },
            $(go.TextBlock,
                { margin: 4, column: 1, font: "500 12px roboto",
                    alignment: go.Spot.Left,
                    // and disallow drawing links from or to this text:
                    fromLinkable: false, toLinkable: false },
                new go.Binding("text", "name")),
        );

        // Return initialization for a RowColumnDefinition, specifying a particular column
        // and adding a Binding of RowColumnDefinition.width to the IDX'th number in the data.widths Array
        function makeWidthBinding(idx) {
            // These two conversion functions are closed over the IDX variable.
            // This source-to-target conversion extracts a number from the Array at the given index.
            function getColumnWidth(arr) {
                if (Array.isArray(arr) && idx < arr.length) return arr[idx];
                return NaN;
            }
            // This target-to-source conversion sets a number in the Array at the given index.
            function setColumnWidth(w, data) {
                var arr = data.widths;
                if (!arr) arr = [];
                if (idx >= arr.length) {
                    for (var i = arr.length; i <= idx; i++) arr[i] = NaN;  // default to NaN
                }
                arr[idx] = w;
                return arr;  // need to return the Array (as the value of data.widths)
            }
            return [
                { column: idx },
                new go.Binding("width", "widths", getColumnWidth).makeTwoWay(setColumnWidth)
            ]
        }
        // This template represents a whole "record".
        myDiagram.nodeTemplate =
            $(go.Node, "Auto",
                new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
                // this rectangular shape surrounds the content of the node
                $(go.Shape,
                    { fill: "#EEEEEE" }),
                // the content consists of a header and a list of items
                $(go.Panel, "Vertical",
                    { stretch: go.GraphObject.Horizontal, alignment: go.Spot.TopLeft },
                    // this is the header for the whole node
                    $(go.Panel, "Auto",
                        { stretch: go.GraphObject.Horizontal },  // as wide as the whole node
                        $(go.Shape,
                            { fill: "#A5C05B", stroke: null }),
                        $(go.TextBlock,
                            {
                                alignment: go.Spot.Center,
                                margin: 5,
                                stroke: "white",
                                textAlign: "center",
                                font: "bold 11pt roboto"
                            },
                            new go.Binding("text", "key"))
                    ),
                    // this Panel holds a Panel for each item object in the itemArray;
                    // each item Panel is defined by the itemTemplate to be a TableRow in this Table
                    $(go.Panel, "Table",
                        {
                            name: "TABLE", stretch: go.GraphObject.Horizontal,
                            minSize: new go.Size(100, 10),
                            defaultAlignment: go.Spot.Left,
                            defaultStretch: go.GraphObject.Horizontal,
                            defaultColumnSeparatorStroke: "gray",
                            defaultRowSeparatorStroke: "gray",
                            itemTemplate: fieldTemplate
                        },
                        new go.Binding("itemArray", "fields")
                    )  // end Table Panel of items
                )  // end Vertical Panel
            );  // end Node
        myDiagram.linkTemplate =
            $(go.Link,
                { relinkableFrom: true, relinkableTo: true, toShortLength: 4 },  // let user reconnect links
                $(go.Shape, { strokeWidth: 1.5 }),
                $(go.Shape, { toArrow: "Standard", stroke: null })
            );
        myDiagram.model =
            $(go.GraphLinksModel,
                {
                    copiesArrays: true,
                    copiesArrayObjects: true,
                    linkFromPortIdProperty: "fromPort",
                    linkToPortIdProperty: "toPort",
                    // automatically update the model that is shown on this page
                    "Changed": function(e) {

                    },
                    nodeDataArray: this.props.nodeData,
                    linkDataArray: this.props.linkData
                });
    }


    render() {

    return (
      <React.Fragment>
          <div id="mapper-diagram" style={{height: '100%', width: '100%'}}></div>
      </React.Fragment>
    );
  }
}


function mapStateToProps(state) {
    const { authentication } = state;
    return {
        authentication
    };
}

const connectedRecordMapper = connect(mapStateToProps)(RecordMapper);
export { connectedRecordMapper as RecordMapper };


// var fieldTemplate =
//     $(go.Panel, "TableRow",  // this Panel is a row in the containing Table
//         new go.Binding("portId", "name"),  // this Panel is a "port"
//         {
//             background: "transparent",  // so this port's background can be picked by the mouse
//             fromSpot: go.Spot.Right,  // links only go from the right side to the left side
//             toSpot: go.Spot.Left,
//             // allow drawing links from or to this port:
//             fromLinkable: true, toLinkable: true
//         },
//         $(go.TextBlock,
//             { margin: 4, column: 1, font: "500 12px roboto",
//                 alignment: go.Spot.Left,
//                 // and disallow drawing links from or to this text:
//                 fromLinkable: false, toLinkable: false },
//             new go.Binding("text", "name")),
//         $(go.TextBlock,
//             { margin: new go.Margin(0, 5), column: 2, font: "12px roboto", alignment: go.Spot.Left },
//             new go.Binding("text", "info"))
//     );
//
// function makeWidthBinding(idx) {
//     // These two conversion functions are closed over the IDX variable.
//     // This source-to-target conversion extracts a number from the Array at the given index.
//     function getColumnWidth(arr) {
//         if (Array.isArray(arr) && idx < arr.length) return arr[idx];
//         return NaN;
//     }
//     // This target-to-source conversion sets a number in the Array at the given index.
//     function setColumnWidth(w, data) {
//         var arr = data.widths;
//         if (!arr) arr = [];
//         if (idx >= arr.length) {
//             for (var i = arr.length; i <= idx; i++) arr[i] = NaN;  // default to NaN
//         }
//         arr[idx] = w;
//         return arr;  // need to return the Array (as the value of data.widths)
//     }
//     return [
//         { column: idx },
//         new go.Binding("width", "widths", getColumnWidth).makeTwoWay(setColumnWidth)
//     ]
// }
//
// myDiagram.nodeTemplate =
//     $(go.Node, "Auto",
//         { movable: false,
//             copyable: false,
//             deletable: false },
//         new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
//         // this rectangular shape surrounds the content of the node
//         $(go.Shape,
//             { fill: "#f5f5f5" }),
//         // the content consists of a header and a list of items
//         $(go.Panel, "Vertical",
//             // this is the header for the whole node
//             $(go.Panel, "Auto",
//                 { stretch: go.GraphObject.Horizontal },  // as wide as the whole node
//                 $(go.Shape,
//                     { fill: "#4caf50", stroke: null }),
//                 $(go.TextBlock,
//                     {
//                         alignment: go.Spot.Center,
//                         margin: 7,
//                         stroke: "white",
//                         textAlign: "center",
//                         font: "bold 11pt roboto"
//                     },
//                     new go.Binding("text", "key"))),
//             // this Panel holds a Panel for each item object in the itemArray;
//             // each item Panel is defined by the itemTemplate to be a TableRow in this Table
//             $(go.Panel, "Table",
//                 {
//                     padding: 4,
//                     minSize: new go.Size(100, 10),
//                     defaultStretch: go.GraphObject.Horizontal,
//                     itemTemplate: fieldTemplate
//                 },
//                 $(go.RowColumnDefinition, makeWidthBinding(0)),
//                 $(go.RowColumnDefinition, makeWidthBinding(1)),
//                 $(go.RowColumnDefinition, makeWidthBinding(2)),
//                 new go.Binding("itemArray", "fields")
//             )  // end Table Panel of items
//         )  // end Vertical Panel
//     );  // end Node
// myDiagram.linkTemplate =
//     $(go.Link,
//         {
//             relinkableFrom: true, relinkableTo: true, // let user reconnect links
//             toShortLength: 4,  fromShortLength: 2
//         },
//         $(go.Shape, { strokeWidth: 1.5 }),
//         $(go.Shape, { toArrow: "Standard", stroke: null })
//     );
// myDiagram.model =
//     $(go.GraphLinksModel,
//         {
//             linkFromPortIdProperty: "fromPort",
//             linkToPortIdProperty: "toPort",
//             nodeDataArray: this.props.nodeData,
//             linkDataArray: this.props.linkData
//         });