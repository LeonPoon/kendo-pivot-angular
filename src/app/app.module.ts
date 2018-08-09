import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { KendoJqueryWrapModule } from './kendo-jquery-wrap/kendo-jquery-wrap.module';
import { HttpModule } from '@angular/http';


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpModule,
    KendoJqueryWrapModule,
  ],
  providers: [],
  bootstrap: [
    AppComponent,
  ]
})
export class AppModule {
}
