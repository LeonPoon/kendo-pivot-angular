/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { PivotGridComponent } from './pivot-grid.component';

describe('PivotGridComponent', () => {
  let component: PivotGridComponent;
  let fixture: ComponentFixture<PivotGridComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PivotGridComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PivotGridComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
