/*
 Highstock JS v10.3.2 (2022-11-28)

 Drag-panes module

 (c) 2010-2021 Highsoft AS
 Author: Kacper Madej

 License: www.highcharts.com/license
*/
(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/drag-panes",["highcharts","highcharts/modules/stock"],function(e){a(e);a.Highcharts=e;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function e(a,f,e,n){a.hasOwnProperty(f)||(a[f]=n.apply(null,e),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:f,module:a[f]}})))}
a=a?a._modules:{};e(a,"Extensions/DragPanes.js",[a["Core/Globals.js"],a["Core/Axis/Axis.js"],a["Core/Axis/AxisDefaults.js"],a["Core/Pointer.js"],a["Core/Utilities.js"]],function(a,f,e,n,b){var x=a.hasTouch,h=b.addEvent,t=b.clamp,y=b.isNumber,z=b.merge,A=b.objectEach,v=b.relativeLength;b=b.wrap;var u=function(){function a(c){this.options=this.lastPos=this.controlLine=this.axis=void 0;this.init(c)}a.prototype.init=function(c,a){this.axis=c;this.options=c.options.resize;this.render();a||this.addMouseEvents()};
a.prototype.render=function(){var c=this.axis,a=c.chart,d=this.options,w=d.x||0,b=d.y,l=t(c.top+c.height+b,a.plotTop,a.plotTop+a.plotHeight),m={};a.styledMode||(m={cursor:d.cursor,stroke:d.lineColor,"stroke-width":d.lineWidth,dashstyle:d.lineDashStyle});this.lastPos=l-b;this.controlLine||(this.controlLine=a.renderer.path().addClass("highcharts-axis-resizer"));this.controlLine.add(c.axisGroup);d=a.styledMode?this.controlLine.strokeWidth():d.lineWidth;m.d=a.renderer.crispLine([["M",c.left+w,l],["L",
c.left+c.width+w,l]],d);this.controlLine.attr(m)};a.prototype.addMouseEvents=function(){var c=this,a=c.controlLine.element,d=c.axis.chart.container,b=[],e,l,m;c.mouseMoveHandler=e=function(a){c.onMouseMove(a)};c.mouseUpHandler=l=function(a){c.onMouseUp(a)};c.mouseDownHandler=m=function(a){c.onMouseDown(a)};b.push(h(d,"mousemove",e),h(d.ownerDocument,"mouseup",l),h(a,"mousedown",m));x&&b.push(h(d,"touchmove",e),h(d.ownerDocument,"touchend",l),h(a,"touchstart",m));c.eventsToUnbind=b};a.prototype.onMouseMove=
function(a){a.touches&&0===a.touches[0].pageX||!this.grabbed||(this.hasDragged=!0,this.updateAxes(this.axis.chart.pointer.normalize(a).chartY-this.options.y))};a.prototype.onMouseUp=function(a){this.hasDragged&&this.updateAxes(this.axis.chart.pointer.normalize(a).chartY-this.options.y);this.grabbed=this.hasDragged=this.axis.chart.activeResizer=null};a.prototype.onMouseDown=function(a){this.axis.chart.pointer.reset(!1,0);this.grabbed=this.axis.chart.activeResizer=!0};a.prototype.updateAxes=function(a){var c=
this,d=c.axis.chart,b=c.options.controlledAxis,e=0===b.next.length?[d.yAxis.indexOf(c.axis)+1]:b.next;b=[c.axis].concat(b.prev);var l=[],m=!1,q=d.plotTop,f=d.plotHeight,h=q+f;a=t(a,q,h);var r=a-c.lastPos;1>r*r||([b,e].forEach(function(b,e){b.forEach(function(b,k){var g=(b=y(b)?d.yAxis[b]:e||k?d.get(b):b)&&b.options;if(g&&"navigator-y-axis"!==g.id){k=b.top;var n=Math.round(v(g.minLength,f));var p=Math.round(v(g.maxLength,f));e?(r=a-c.lastPos,g=Math.round(t(b.len-r,n,p)),k=b.top+r,k+g>h&&(p=h-g-k,a+=
p,k+=p),k<q&&(k=q,k+g>h&&(g=f)),g===n&&(m=!0),l.push({axis:b,options:{top:100*(k-q)/f+"%",height:100*g/f+"%"}})):(g=Math.round(t(a-k,n,p)),g===p&&(m=!0),a=k+g,l.push({axis:b,options:{height:100*g/f+"%"}}))}})}),m||(l.forEach(function(a){a.axis.update(a.options,!1)}),d.redraw(!1)))};a.prototype.destroy=function(){var a=this;delete a.axis.resizer;this.eventsToUnbind&&this.eventsToUnbind.forEach(function(a){a()});a.controlLine.destroy();A(a,function(b,c){a[c]=null})};a.resizerOptions={minLength:"10%",
maxLength:"100%",resize:{controlledAxis:{next:[],prev:[]},enabled:!1,cursor:"ns-resize",lineColor:"#cccccc",lineDashStyle:"Solid",lineWidth:4,x:0,y:0}};return a}();f.keepProps.push("resizer");h(f,"afterRender",function(){var a=this.resizer,b=this.options.resize;b&&(b=!1!==b.enabled,a?b?a.init(this,!0):a.destroy():b&&(this.resizer=new u(this)))});h(f,"destroy",function(a){!a.keepEvents&&this.resizer&&this.resizer.destroy()});b(n.prototype,"runPointActions",function(a){this.chart.activeResizer||a.apply(this,
Array.prototype.slice.call(arguments,1))});b(n.prototype,"drag",function(a){this.chart.activeResizer||a.apply(this,Array.prototype.slice.call(arguments,1))});z(!0,e.defaultYAxisOptions,u.resizerOptions);a.AxisResizer=u;return a.AxisResizer});e(a,"masters/modules/drag-panes.src.js",[],function(){})});
//# sourceMappingURL=drag-panes.js.map