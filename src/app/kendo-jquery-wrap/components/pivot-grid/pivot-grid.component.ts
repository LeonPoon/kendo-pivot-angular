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
    jQuery(this.divElement.nativeElement).kendoPivotGrid({});
  }

}
