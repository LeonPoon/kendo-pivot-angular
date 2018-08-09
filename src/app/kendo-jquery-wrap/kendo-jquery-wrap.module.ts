import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PivotGridComponent } from './components/pivot-grid/pivot-grid.component';

@NgModule({
  imports: [
    CommonModule,
  ],
  declarations: [
    PivotGridComponent,
  ],
  exports: [
    PivotGridComponent,
  ]
})
export class KendoJqueryWrapModule { }
