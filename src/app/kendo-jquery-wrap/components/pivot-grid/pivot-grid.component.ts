import { Component, OnInit, ViewChild, AfterViewInit, ElementRef } from '@angular/core';
import * as jQuery from 'jquery';
import '@progress/kendo-ui';

@Component({
  selector: 'kendo-jquery-wrap-pivot-grid',
  templateUrl: './pivot-grid.component.html',
  styleUrls: ['./pivot-grid.component.css']
})
export class PivotGridComponent implements OnInit, AfterViewInit {

  @ViewChild('div') divElement: ElementRef;

  constructor() { }

  ngOnInit() {
  }

  ngAfterViewInit(): void {
    jQuery(this.divElement.nativeElement).kendoPivotGrid({
      height: '100%', // define the height of the widget
      dataSource: {
          type: 'xmla', // define the type
          columns: [{ name: '[Date].[Calendar]' }], // specify a dimesion on columns
          rows: [{ name: '[Product].[Category]' }], // specify a dimesion on rows
          measures: ['[Measures].[Internet Sales Amount]'], // specify a measure to display
          transport: {
              connection: {
                  catalog: 'Adventure Works DW 2008R2', // specify the name of the catalog
                  cube: 'Adventure Works' // specify the name of the cube
              },
              read: {
                  url: 'https://demos.telerik.com/olap/msmdpump.dll', // define the URL of the service
                  dataType: 'text',
                  contentType: 'text/xml',
                  type: 'POST'
              }
          },
          schema: {
              type: 'xmla' // specify the type of the schema
          },
      }
    });
  }

}
