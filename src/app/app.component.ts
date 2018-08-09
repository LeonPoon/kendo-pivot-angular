import { Component } from '@angular/core';
import * as demoData from '../../demo/demo1.json';
import { Http } from '@angular/http';


const schema: kendo.data.PivotSchema = {
  axes: 'axes', // axes are returned in the 'axes' field of the response
  data: 'data',
  dimensions: 'dimensions',
  levels: 'levels',
  hierarchies: 'hierarchies',
  measures: 'measures',
};


const {columns, rows, measures} = {
  columns: [{ name: '[Date].[Calendar]', expand: true }, { name: '[Product].[Category]' }],
  rows: [
    { name: '[Sales Reason].[Sales Reasons]' },
    { name: '[Destination Currency].[Destination Currency Code]' },
  ],
  measures: ['[Measures].[Reseller Freight Cost]'],
};


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  opts;

  constructor(
    private http: Http,
  ) {
    this.opts = this.ajaxOpts();
  }

  jsonOpts() {
    const opts = {
      height: 580,
      dataSource: {
        columns, rows, measures,
        transport: {
          read: (options: kendo.data.DataSourceTransportOptions) => options.success((demoData as any).data)
        },
        schema,
      }
    };
    return opts;
  }

  ajaxOpts() {
    const opts = {
      height: 580,
      dataSource: {
        columns, rows, measures,
        transport: {
          read: {
            url: 'http://localhost:5000',
            dataType: 'json',
            contentType: 'application/json',
          }
        },
        schema,
      }
    };
    return opts;
  }

  telerikOpts() {
    return {
      filterable: true,
      sortable: true,
      columnWidth: 200,
      height: 580,
      dataSource: {
        type: 'xmla',
        columns, rows, measures,
        transport: {
          connection: {
            catalog: 'Adventure Works DW 2008R2',
            cube: 'Adventure Works'
          },
          read: 'https://demos.telerik.com/olap/msmdpump.dll'
        },
        schema: {
          type: 'xmla'
        },
        error: function (e) {
          alert('error: ' + kendo.stringify(e.errors[0]));
        }
      }
    };
  }
}
