import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

const defaultProps = {};

var names = {};

function traverseDom(node, parentName, dataArray) {
    if (parentName === undefined) parentName = null;
    if (dataArray === undefined) dataArray = [];
    // skip everything but HTML Elements
    if (!(node instanceof Element)) return;
    // Ignore the navigation menus
    if (node.id === "navindex" || node.id === "navtop") return;
    // add this node to the nodeDataArray
    var name = getName(node);
    var data = { key: name, name: name };
    dataArray.push(data);
    // add a link to its parent
    if (parentName !== null) {
        data.parent = parentName;
    }
    // find all children
    var l = node.childNodes.length;
    for (var i = 0; i < l; i++) {
        traverseDom(node.childNodes[i], name, dataArray);
    }
    return dataArray;
}


function getName(node) {
    var n = node.nodeName;
    if (node.id) n = n + " (" + node.id + ")";
    var namenum = n;  // make sure the name is unique
    var i = 1;
    while (names[namenum] !== undefined) {
        namenum = n + i;
        i++;
    }
    names[namenum] = node;
    return namenum;
}


class TreeViewer extends Component {
    constructor(props) {
        super(props);
    }



    componentDidMount() {
        var context = this;
        var $ = go.GraphObject.make;  // for conciseness in defining templates
        var myDiagram =
            $(go.Diagram, "tree-diagram",
                {
                    initialAutoScale: go.Diagram.UniformToFill,
                    // define the layout for the diagram
                    layout: $(go.TreeLayout, { nodeSpacing: 5, layerSpacing: 30 })
                });
        // Define a simple node template consisting of text followed by an expand/collapse button
        myDiagram.nodeTemplate =
            $(go.Node, "Horizontal",
                // { selectionChanged: nodeSelectionChanged },  // this event handler is defined below
                $(go.Panel, "Auto",
                    $(go.Shape, { fill: "#1F4963", stroke: null }),
                    $(go.TextBlock,
                        { font: "bold 13px Helvetica, bold Arial, sans-serif",
                            stroke: "white", margin: 3 },
                        new go.Binding("text", "key"))
                ),
                $("TreeExpanderButton")
            );
        // Define a trivial link template with no arrowhead.
        myDiagram.linkTemplate =
            $(go.Link,
                { selectable: false },
                $(go.Shape));  // the link shape
        // create the model for the DOM tree

        myDiagram.model =
            $(go.TreeModel, {
                isReadOnly: true,  // don't allow the user to delete or copy nodes
                // build up the tree in an Array of node data
                nodeDataArray: this.props.treeData
            });

    }


    render() {

    return (
      <React.Fragment>
          <div id="tree-diagram" style={{height: '100%', width: '100%'}}></div>
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

const connectedTreeViewer = connect(mapStateToProps)(TreeViewer);
export { connectedTreeViewer as TreeViewer };